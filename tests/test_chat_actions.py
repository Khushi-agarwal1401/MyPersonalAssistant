"""Tests for renaming and deleting individual chats (right-click menu on the history list).

These use a real, hidden Tk window. If this machine has no display, they are skipped.
"""
import json

import pytest

tk = pytest.importorskip("tkinter")
import desktop_app  # noqa: E402


def make_chat(chat_id, title):
    return {"id": chat_id, "title": title, "messages": [
        {"role": "user", "content": f"question for {title}"},
        {"role": "assistant", "content": f"answer for {title}"}]}


@pytest.fixture
def app(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)  # history and settings files go to a temporary folder
    monkeypatch.setattr(desktop_app.JugnuApp, "warm_up", lambda self: None)  # no Ollama call
    try:
        root = tk.Tk()
    except tk.TclError:
        pytest.skip("no display available for Tk")
    root.withdraw()
    window = desktop_app.JugnuApp(root)
    window.chats = [make_chat("a", "Alpha"), make_chat("b", "Beta"), make_chat("c", "Gamma")]
    window.current_id = "c"
    window.draft_chat = None
    window.save_history()
    window.refresh_history_list()
    yield window
    root.destroy()


def saved_history():
    with open(desktop_app.HISTORY_FILE, encoding="utf-8") as f:
        return json.load(f)


def test_rename_changes_only_that_title_and_saves(app, monkeypatch):
    monkeypatch.setattr(app, "ask_chat_title", lambda initial: "  My   new   name ")
    app.rename_chat("a")
    assert [c["title"] for c in app.chats] == ["My new name", "Beta", "Gamma"]
    assert [c["title"] for c in saved_history()] == ["My new name", "Beta", "Gamma"]
    assert len(app.find_chat("a")["messages"]) == 2


def test_rename_does_not_open_the_chat(app, monkeypatch):
    monkeypatch.setattr(app, "ask_chat_title", lambda initial: "Renamed")
    app.rename_chat("a")
    assert app.current_id == "c"


@pytest.mark.parametrize("answer", [None, "", "     ", "Alpha"])
def test_rename_ignores_cancel_empty_and_unchanged(app, monkeypatch, answer):
    monkeypatch.setattr(app, "ask_chat_title", lambda initial: answer)
    app.rename_chat("a")
    assert app.find_chat("a")["title"] == "Alpha"


def test_rename_caps_very_long_titles(app, monkeypatch):
    monkeypatch.setattr(app, "ask_chat_title", lambda initial: "x" * 200)
    app.rename_chat("a")
    assert len(app.find_chat("a")["title"]) == desktop_app.MAX_TITLE_LENGTH


def test_long_titles_are_shortened_in_the_list(app, monkeypatch):
    monkeypatch.setattr(app, "ask_chat_title", lambda initial: "y" * 50)
    app.rename_chat("a")
    row = app.history_list.get(2)  # the list shows the oldest chat last
    assert row.endswith("…") and len(row) == len("  ◌  ") + desktop_app.MAX_LIST_TITLE


def test_delete_another_chat_keeps_everything_else(app, monkeypatch):
    monkeypatch.setattr(desktop_app.messagebox, "askyesno", lambda *a, **k: True)
    before = {c["id"]: json.dumps(c) for c in app.chats}
    app.delete_chat("b")
    assert [c["id"] for c in app.chats] == ["a", "c"]
    assert all(json.dumps(c) == before[c["id"]] for c in app.chats)
    assert app.current_id == "c"
    assert [c["id"] for c in saved_history()] == ["a", "c"]


def test_delete_open_chat_shows_a_fresh_empty_chat(app, monkeypatch):
    monkeypatch.setattr(desktop_app.messagebox, "askyesno", lambda *a, **k: True)
    app.delete_chat("c")
    assert app.find_chat("c") is None
    assert app.current_id != "c"
    assert app.current_chat()["messages"] == []
    assert [c["id"] for c in saved_history()] == ["a", "b"]
    assert [c["id"] for c in app.chats] == ["a", "b"]  # the empty draft is not saved as a chat


def test_delete_declined_changes_nothing(app, monkeypatch):
    monkeypatch.setattr(desktop_app.messagebox, "askyesno", lambda *a, **k: False)
    app.delete_chat("a")
    assert [c["id"] for c in app.chats] == ["a", "b", "c"]
    assert len(saved_history()) == 3


def test_delete_asks_with_the_chat_title(app, monkeypatch):
    asked = []
    monkeypatch.setattr(desktop_app.messagebox, "askyesno", lambda title, message: asked.append(message) or False)
    app.delete_chat("b")
    assert "Beta" in asked[0]


def test_delete_last_chat_leaves_empty_history(app, monkeypatch):
    monkeypatch.setattr(desktop_app.messagebox, "askyesno", lambda *a, **k: True)
    for chat_id in ("a", "b", "c"):
        app.delete_chat(chat_id)
    assert app.chats == [] and saved_history() == []
    assert app.current_chat()["messages"] == []


def test_actions_on_a_missing_chat_do_nothing(app, monkeypatch):
    monkeypatch.setattr(desktop_app.messagebox, "askyesno", lambda *a, **k: True)
    monkeypatch.setattr(app, "ask_chat_title", lambda initial: "x")
    app.rename_chat("nope")
    app.delete_chat("nope")
    assert [c["id"] for c in app.chats] == ["a", "b", "c"]


def test_renamed_title_survives_a_restart(app, monkeypatch):
    monkeypatch.setattr(app, "ask_chat_title", lambda initial: "Kept after restart")
    app.rename_chat("b")
    assert [c["title"] for c in app.load_history()] == ["Alpha", "Kept after restart", "Gamma"]