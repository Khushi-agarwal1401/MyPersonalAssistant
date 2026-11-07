"""Tests for TTSManager's speed / volume / voice settings, using a fake pyttsx3 engine."""
import threading
import time
import types

import tts


class FakeVoice:
    def __init__(self, voice_id, name):
        self.id, self.name = voice_id, name


class FakeEngine:
    """Records the settings that were active each time a sentence is spoken."""

    def __init__(self):
        self.props = {"rate": 200, "volume": 1.0, "voice": "voice-default"}
        self.spoken = []                    # (sentence, rate, volume, voice)
        self.fail_voice = set()             # voice ids that setProperty rejects
        self.gate = None                    # optional Event: first sentence waits for it
        self._current = None

    def getProperty(self, name):
        if name == "voices":
            return [FakeVoice("voice-default", "Default Voice"), FakeVoice("voice-two", "Second Voice")]
        return self.props[name]

    def setProperty(self, name, value):
        if name == "voice" and value in self.fail_voice:
            raise RuntimeError("voice not installed")
        self.props[name] = value

    def connect(self, *_args):
        pass

    def say(self, sentence):
        self._current = sentence

    def runAndWait(self):
        if self.gate is not None:
            gate, self.gate = self.gate, None
            gate.wait(timeout=5)
        self.spoken.append((self._current, self.props["rate"], self.props["volume"], self.props["voice"]))

    def stop(self):
        pass


def make_manager(monkeypatch, engine=None, **kwargs):
    engine = engine or FakeEngine()
    fake_module = types.SimpleNamespace(init=lambda: engine)
    monkeypatch.setattr(tts, "pyttsx3", fake_module)
    return tts.TTSManager(**kwargs), engine


def wait_until(condition, timeout=3.0):
    end = time.time() + timeout
    while time.time() < end:
        if condition():
            return True
        time.sleep(0.01)
    return False


def test_starting_values_reach_the_engine(monkeypatch):
    manager, engine = make_manager(monkeypatch, rate=140, volume=0.5, voice_id="voice-two")
    manager.speak("Hello.")
    assert wait_until(lambda: engine.spoken)
    assert engine.spoken[0][1:] == (140, 0.5, "voice-two")


def test_installed_voices_are_listed(monkeypatch):
    manager, _ = make_manager(monkeypatch)
    assert wait_until(lambda: manager.voices)
    assert manager.voices == [("voice-default", "Default Voice"), ("voice-two", "Second Voice")]


def test_change_applies_to_the_next_sentence_without_restart(monkeypatch):
    engine = FakeEngine()
    gate = threading.Event()
    engine.gate = gate
    manager, _ = make_manager(monkeypatch, engine=engine, rate=175, volume=1.0)
    manager.speak("First one. Second one.")
    time.sleep(0.1)  # the worker is now inside the first sentence
    manager.apply_settings(250, 0.3, "voice-two")
    gate.set()
    assert wait_until(lambda: len(engine.spoken) == 2)
    assert engine.spoken[0][1:] == (175, 1.0, "voice-default")
    assert engine.spoken[1][1:] == (250, 0.3, "voice-two")


def test_missing_saved_voice_falls_back_to_default(monkeypatch):
    manager, engine = make_manager(monkeypatch, voice_id="voice-that-was-uninstalled")
    manager.speak("Hello.")
    assert wait_until(lambda: engine.spoken)
    assert engine.spoken[0][3] == "voice-default"


def test_going_back_to_default_voice(monkeypatch):
    manager, engine = make_manager(monkeypatch, voice_id="voice-two")
    manager.speak("One.")
    assert wait_until(lambda: len(engine.spoken) == 1)
    manager.apply_settings(175, 1.0, None)
    manager.speak("Two.")
    assert wait_until(lambda: len(engine.spoken) == 2)
    assert engine.spoken[1][3] == "voice-default"


def test_engine_rejecting_a_voice_does_not_crash(monkeypatch):
    engine = FakeEngine()
    engine.fail_voice = {"voice-two"}
    manager, _ = make_manager(monkeypatch, engine=engine, voice_id="voice-two", rate=150)
    manager.speak("Still works.")
    assert wait_until(lambda: engine.spoken)
    assert engine.spoken[0][1] == 150            # the other settings still applied
    assert engine.spoken[0][3] == "voice-default"


def test_values_are_clamped(monkeypatch):
    manager, _ = make_manager(monkeypatch, rate=9999, volume=7)
    assert manager.rate == tts.RATE_MAX and manager.volume == 1.0
    manager.apply_settings(1, -3, None)
    assert manager.rate == tts.RATE_MIN and manager.volume == 0.0


def test_settings_survive_stop(monkeypatch):
    manager, engine = make_manager(monkeypatch)
    manager.apply_settings(220, 0.6, None)
    manager.stop()
    manager.speak("After stop.")
    assert wait_until(lambda: engine.spoken)
    assert engine.spoken[0][1:3] == (220, 0.6)


def test_unavailable_tts_does_nothing(monkeypatch):
    monkeypatch.setattr(tts, "pyttsx3", None)
    manager = tts.TTSManager()
    manager.apply_settings(200, 0.5, None)
    manager.speak("silent")
    assert manager.available is False and manager.voices == []