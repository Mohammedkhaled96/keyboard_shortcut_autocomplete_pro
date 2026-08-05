import globalPluginHandler
import api
import ui
import speech
import config
import gui
import wx
import os
import json
import codecs
import time
import threading
from scriptHandler import script
import textInfos
import keyboardHandler
from logHandler import log
import core
import queueHandler
import re

CONFIG_DIR = config.getUserDefaultConfigPath()
CONFIG_FILE = os.path.join(CONFIG_DIR, "keyboardShortcutsPro.json")

class ShortcutData:
    
    def __init__(self):
        self.shortcuts = {}
        self.enabled = True
        self._lock = threading.RLock()
        self.load()
    
    def load(self):
        with self._lock:
            try:
                if os.path.exists(CONFIG_FILE):
                    with codecs.open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        self.shortcuts = data.get('shortcuts', self.get_defaults())
                        self.enabled = data.get('enabled', True)
                else:
                    self.shortcuts = self.get_defaults()
                    self.save()
            except Exception as e:
                log.error(f"Error loading shortcuts: {e}")
                self.shortcuts = self.get_defaults()
                self.enabled = True
    
    def save(self):
        with self._lock:
            try:
                data = {
                    'shortcuts': self.shortcuts,
                    'enabled': self.enabled
                }
                with codecs.open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                return True
            except Exception as e:
                log.error(f"Error saving shortcuts: {e}")
                return False
    
    def get_defaults(self):
        return {
            "brb": "be right back",
            "omw": "on my way",
            "ty": "thank you",
            "yw": "you're welcome",
            "pls": "please",
            "btw": "by the way",
            "fyi": "for your information",
            "asap": "as soon as possible",
            "etc": "et cetera",
            "eg": "for example",
            "ie": "that is",
            "ps": "postscript",
            "rsvp": "please respond",
            "eta": "estimated time of arrival",
            "diy": "do it yourself",
            "faq": "frequently asked questions",
            "tba": "to be announced",
            "tbd": "to be determined",
            "w/": "with",
            "w/o": "without",
            "b/c": "because",
            "b/w": "between",
            "c/o": "care of",
            "n/a": "not applicable",
            "aka": "also known as",
            "imho": "in my humble opinion",
            "imo": "in my opinion",
            "lol": "laughing out loud",
            "gtg": "got to go",
            "ttyl": "talk to you later",
            "cya": "see you",
            "np": "no problem",
            "nvm": "never mind",
            "jk": "just kidding",
            "tbh": "to be honest",
            "idk": "I don't know",
            "ikr": "I know, right?",
            "ISA": "In Shaa Allah",
            "بسملله": "بسم الله الرحمن الرحيم",
            "السلام عليكم": "السلام عليكم ورحمة الله وبركاته",
            "وعليكم": "وعليكم السلام ورحمة الله وبركاته",
            "جزاكم": "جزاكم الله خيرا",
            "بارك": "بارك الله فيك",
            "ماشاءالله": "ما شاء الله",
            "سبحانالله": "سبحان الله",
            "الحمدلله": "الحمد لله",
            "لااله": "لا إله إلا الله",
            "اللهم صل": "اللهم صل وسلم على نبينا محمد",
            "استغفرالله": "استغفر الله العظيم",            "sa": "selamun Aleyküm",
            "as": "aleyküm selam",
            "kg": "kolay gelsin",
            "hg": "hoş geldin",
            "hb": "hoş buldum",
            "ao": "afiyet olsun",
            "kib": "kendine iyi bak",
            "tşk": "teşekkür ederim",
            "moh@": "mohammed.khaled.mahmoud1996@gmail.com"
        }
    
    def add(self, shortcut, expansion):
        with self._lock:
            self.shortcuts[shortcut] = expansion
            return self.save()
    
    def remove(self, shortcut):
        with self._lock:
            if shortcut in self.shortcuts:
                del self.shortcuts[shortcut]
                return self.save()
            return False
    
    def get(self, shortcut):
        with self._lock:
            return self.shortcuts.get(shortcut)
    
    def get_all(self):
        with self._lock:
            return self.shortcuts.copy()
    
    def toggle_enabled(self):
        with self._lock:
            self.enabled = not self.enabled
            self.save()
            return self.enabled
    
    def is_enabled(self):
        with self._lock:
            return self.enabled
    
    def import_shortcuts(self, shortcuts_dict):
        with self._lock:
            self.shortcuts.update(shortcuts_dict)
            return self.save()
    
    def export_shortcuts(self):
        with self._lock:
            return self.shortcuts.copy()

class ShortcutManagerDialog(wx.Dialog):
    
    def __init__(self, parent, shortcut_data):
        super(ShortcutManagerDialog, self).__init__(
            parent,
            title="Keyboard Shortcuts Manager",
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        )
        
        self.shortcut_data = shortcut_data
        self.SetSize((700, 500))
        self.init_ui()
        self.Centre()
    
    def init_ui(self):
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        header_panel = wx.Panel(self)
        header_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        status = "Enabled" if self.shortcut_data.is_enabled() else "Disabled"
        self.status_text = wx.StaticText(header_panel, label=f"Status: {status}")
        header_sizer.Add(self.status_text, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        
        header_sizer.AddStretchSpacer()
        
        self.toggle_btn = wx.Button(header_panel, label="&Disable" if self.shortcut_data.is_enabled() else "&Enable")
        self.toggle_btn.Bind(wx.EVT_BUTTON, self.on_toggle)
        header_sizer.Add(self.toggle_btn, 0, wx.ALL, 5)
        
        header_panel.SetSizer(header_sizer)
        main_sizer.Add(header_panel, 0, wx.EXPAND | wx.ALL, 10)
        
        search_panel = wx.Panel(self)
        search_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        search_label = wx.StaticText(search_panel, label="&Search:")
        search_sizer.Add(search_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        
        self.search_ctrl = wx.TextCtrl(search_panel)
        self.search_ctrl.Bind(wx.EVT_TEXT, self.on_search)
        search_sizer.Add(self.search_ctrl, 1, wx.ALL | wx.EXPAND, 5)
        
        search_panel.SetSizer(search_sizer)
        main_sizer.Add(search_panel, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        
        self.listCtrl = wx.ListCtrl(
            self,
            style=wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_HRULES | wx.LC_VRULES
        )
        self.listCtrl.InsertColumn(0, "Shortcut", width=200)
        self.listCtrl.InsertColumn(1, "Expands to", width=450)
        
        self.all_shortcuts = []
        self.refresh_list()
        
        main_sizer.Add(self.listCtrl, 1, wx.EXPAND | wx.ALL, 10)
        
        btn_panel = wx.Panel(self)
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.add_btn = wx.Button(btn_panel, label="&Add")
        self.add_btn.Bind(wx.EVT_BUTTON, self.on_add)
        btn_sizer.Add(self.add_btn, 0, wx.ALL, 5)
        
        self.edit_btn = wx.Button(btn_panel, label="&Edit")
        self.edit_btn.Bind(wx.EVT_BUTTON, self.on_edit)
        btn_sizer.Add(self.edit_btn, 0, wx.ALL, 5)
        
        self.delete_btn = wx.Button(btn_panel, label="&Delete")
        self.delete_btn.Bind(wx.EVT_BUTTON, self.on_delete)
        btn_sizer.Add(self.delete_btn, 0, wx.ALL, 5)
        
        btn_sizer.AddStretchSpacer()
        
        self.import_btn = wx.Button(btn_panel, label="&Import...")
        self.import_btn.Bind(wx.EVT_BUTTON, self.on_import)
        btn_sizer.Add(self.import_btn, 0, wx.ALL, 5)
        
        self.export_btn = wx.Button(btn_panel, label="E&xport...")
        self.export_btn.Bind(wx.EVT_BUTTON, self.on_export)
        btn_sizer.Add(self.export_btn, 0, wx.ALL, 5)
        
        btn_panel.SetSizer(btn_sizer)
        main_sizer.Add(btn_panel, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        
        std_btn_sizer = self.CreateStdDialogButtonSizer(wx.OK | wx.CANCEL)
        main_sizer.Add(std_btn_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        
        self.SetSizer(main_sizer)
        
        self.listCtrl.Bind(wx.EVT_KEY_DOWN, self.on_key_down)
        self.listCtrl.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_edit)
        self.listCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_selection_changed)
        
        self.update_button_states()
        
        self.listCtrl.SetFocus()
    
    def refresh_list(self, filter_text=""):
        self.listCtrl.DeleteAllItems()
        shortcuts = self.shortcut_data.get_all()
        
        self.all_shortcuts = [(k, v) for k, v in shortcuts.items()]
        self.all_shortcuts.sort(key=lambda x: x[0].lower())
        
        filtered = self.all_shortcuts
        if filter_text:
            filter_lower = filter_text.lower()
            filtered = [(k, v) for k, v in self.all_shortcuts 
                       if filter_lower in k.lower() or filter_lower in v.lower()]
        
        for idx, (shortcut, expansion) in enumerate(filtered):
            index = self.listCtrl.InsertItem(idx, shortcut)
            self.listCtrl.SetItem(index, 1, expansion)
        
        if self.listCtrl.GetItemCount() > 0:
            self.listCtrl.Select(0)
            self.listCtrl.Focus(0)
    
    def update_button_states(self):
        has_selection = self.listCtrl.GetFirstSelected() >= 0
        self.edit_btn.Enable(has_selection)
        self.delete_btn.Enable(has_selection)
    
    def on_selection_changed(self, event):
        self.update_button_states()
        event.Skip()
    
    def on_toggle(self, event):
        enabled = self.shortcut_data.toggle_enabled()
        self.status_text.SetLabel(f"Status: {'Enabled' if enabled else 'Disabled'}")
        self.toggle_btn.SetLabel("&Disable" if enabled else "&Enable")
        ui.message(f"Keyboard shortcuts {'enabled' if enabled else 'disabled'}")
    
    def on_search(self, event):
        filter_text = self.search_ctrl.GetValue()
        self.refresh_list(filter_text)
    
    def on_key_down(self, event):
        key = event.GetKeyCode()
        if key == wx.WXK_F2:
            self.on_edit(None)
        elif key == wx.WXK_DELETE:
            self.on_delete(None)
        elif key == ord('A') and event.ControlDown():
            self.on_add(None)
        else:
            event.Skip()
    
    def on_add(self, event):
        dlg = ShortcutEntryDialog(self, "Add Shortcut")
        if dlg.ShowModal() == wx.ID_OK:
            shortcut, expansion = dlg.get_values()
            if shortcut and expansion:
                if self.shortcut_data.get(shortcut):
                    wx.MessageBox(
                        f"Shortcut '{shortcut}' already exists. Use Edit to modify it.",
                        "Duplicate Shortcut",
                        wx.OK | wx.ICON_WARNING
                    )
                else:
                    self.shortcut_data.add(shortcut, expansion)
                    self.refresh_list(self.search_ctrl.GetValue())
                    ui.message(f"Shortcut '{shortcut}' added")
        dlg.Destroy()
    
    def on_edit(self, event):
        selection = self.listCtrl.GetFirstSelected()
        if selection >= 0:
            shortcut = self.listCtrl.GetItemText(selection, 0)
            expansion = self.listCtrl.GetItemText(selection, 1)
            
            dlg = ShortcutEntryDialog(self, "Edit Shortcut", shortcut, expansion)
            if dlg.ShowModal() == wx.ID_OK:
                new_shortcut, new_expansion = dlg.get_values()
                if new_shortcut and new_expansion:
                    if shortcut != new_shortcut and self.shortcut_data.get(new_shortcut):
                        wx.MessageBox(
                            f"Shortcut '{new_shortcut}' already exists.",
                            "Duplicate Shortcut",
                            wx.OK | wx.ICON_WARNING
                        )
                    else:
                        if shortcut != new_shortcut:
                            self.shortcut_data.remove(shortcut)
                        self.shortcut_data.add(new_shortcut, new_expansion)
                        self.refresh_list(self.search_ctrl.GetValue())
                        ui.message(f"Shortcut updated")
            dlg.Destroy()
    
    def on_delete(self, event):
        selection = self.listCtrl.GetFirstSelected()
        if selection >= 0:
            shortcut = self.listCtrl.GetItemText(selection, 0)
            
            if wx.MessageBox(
                f"Are you sure you want to delete the shortcut '{shortcut}'?",
                "Confirm Delete",
                wx.YES_NO | wx.ICON_QUESTION
            ) == wx.YES:
                self.shortcut_data.remove(shortcut)
                self.refresh_list(self.search_ctrl.GetValue())
                ui.message(f"Shortcut '{shortcut}' deleted")
    
    def on_import(self, event):
        wildcard = "JSON files (*.json)|*.json"
        dlg = wx.FileDialog(
            self,
            "Import Shortcuts",
            wildcard=wildcard,
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
        )
        
        if dlg.ShowModal() == wx.ID_OK:
            try:
                with codecs.open(dlg.GetPath(), 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                if isinstance(data, dict):
                    shortcuts = data.get('shortcuts', data)
                else:
                    shortcuts = data
                
                if not isinstance(shortcuts, dict):
                    raise ValueError("Invalid file format")
                
                count = len(shortcuts)
                if wx.MessageBox(
                    f"Import {count} shortcuts? This will merge with existing shortcuts.",
                    "Confirm Import",
                    wx.YES_NO | wx.ICON_QUESTION
                ) == wx.YES:
                    self.shortcut_data.import_shortcuts(shortcuts)
                    self.refresh_list()
                    ui.message(f"Imported {count} shortcuts")
            
            except Exception as e:
                wx.MessageBox(
                    f"Error importing shortcuts: {str(e)}",
                    "Import Error",
                    wx.OK | wx.ICON_ERROR
                )
        
        dlg.Destroy()
    
    def on_export(self, event):
        wildcard = "JSON files (*.json)|*.json"
        dlg = wx.FileDialog(
            self,
            "Export Shortcuts",
            wildcard=wildcard,
            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
        )
        
        if dlg.ShowModal() == wx.ID_OK:
            try:
                data = {
                    'shortcuts': self.shortcut_data.export_shortcuts(),
                    'enabled': self.shortcut_data.is_enabled()
                }
                
                with codecs.open(dlg.GetPath(), 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                
                ui.message(f"Shortcuts exported successfully")
            
            except Exception as e:
                wx.MessageBox(
                    f"Error exporting shortcuts: {str(e)}",
                    "Export Error",
                    wx.OK | wx.ICON_ERROR
                )
        
        dlg.Destroy()

class ShortcutEntryDialog(wx.Dialog):
    
    def __init__(self, parent, title, shortcut="", expansion=""):
        super(ShortcutEntryDialog, self).__init__(
            parent,
            title=title,
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        )
        
        self.SetSize((500, 350))
        
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        shortcut_sizer = wx.BoxSizer(wx.HORIZONTAL)
        shortcut_label = wx.StaticText(self, label="&Shortcut:")
        shortcut_sizer.Add(shortcut_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        
        self.shortcut_text = wx.TextCtrl(self, value=shortcut, size=(200, -1))
        shortcut_sizer.Add(self.shortcut_text, 1, wx.ALL | wx.EXPAND, 5)
        
        main_sizer.Add(shortcut_sizer, 0, wx.EXPAND | wx.ALL, 10)
        
        expansion_label = wx.StaticText(self, label="&Expands to:")
        main_sizer.Add(expansion_label, 0, wx.LEFT | wx.RIGHT, 15)
        
        self.expansion_text = wx.TextCtrl(
            self,
            value=expansion,
            style=wx.TE_MULTILINE,
            size=(-1, 150)
        )
        main_sizer.Add(self.expansion_text, 1, wx.EXPAND | wx.ALL, 15)
        
        help_text = wx.StaticText(
            self,
            label="Tip: Use \\n for new lines, \\t for tabs"
        )
        help_text.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_GRAYTEXT))
        main_sizer.Add(help_text, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 15)
        
        btn_sizer = self.CreateStdDialogButtonSizer(wx.OK | wx.CANCEL)
        main_sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        
        self.SetSizer(main_sizer)
        self.Centre()
        
        self.shortcut_text.SetFocus()
        self.shortcut_text.SelectAll()
        
        self.Bind(wx.EVT_BUTTON, self.on_ok, id=wx.ID_OK)
    
    def on_ok(self, event):
        shortcut = self.shortcut_text.GetValue().strip()
        expansion = self.expansion_text.GetValue().strip()
        
        if not shortcut:
            wx.MessageBox(
                "Please enter a shortcut.",
                "Validation Error",
                wx.OK | wx.ICON_WARNING
            )
            self.shortcut_text.SetFocus()
            return
        
        if not expansion:
            wx.MessageBox(
                "Please enter the expansion text.",
                "Validation Error",
                wx.OK | wx.ICON_WARNING
            )
            self.expansion_text.SetFocus()
            return
        
        expansion = expansion.replace('\\n', '\n').replace('\\t', '\t')
        self.expansion_text.SetValue(expansion)
        
        event.Skip()
    
    def get_values(self):
        return (
            self.shortcut_text.GetValue().strip(),
            self.expansion_text.GetValue().strip()
        )

class TextExpander:
    
    @staticmethod
    def expand_text_smart(shortcut, expansion):
        return TextExpander.expand_text_fallback(shortcut, expansion)
    
    @staticmethod
    def expand_text_fallback(shortcut, expansion):
        try:
            shortcut_len = len(shortcut)
            for _ in range(shortcut_len):
                keyboardHandler.KeyboardInputGesture.fromName("backspace").send()
            
            time.sleep(0.05)
            
            old_clip = api.getClipData()
            api.copyToClip(expansion)
            time.sleep(0.05)
            keyboardHandler.KeyboardInputGesture.fromName("control+v").send()
            
            if old_clip is not None:
                wx.CallLater(200, lambda: api.copyToClip(old_clip))
            
            return True
            
        except Exception as e:
            log.error(f"Error in text expansion fallback: {e}")
            return False

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    
    def __init__(self):
        super(GlobalPlugin, self).__init__()
        self.shortcut_data = ShortcutData()
        self.last_expanded = None
        log.info("Keyboard Shortcut Autocomplete Professional loaded")
    
    @script(
        description="Expand the typed shortcut",
        category="Text Editing",
        gesture="kb:nvda+e"
    )
    def script_expandShortcut(self, gesture):
        if not self.shortcut_data.is_enabled():
            ui.message("Keyboard shortcuts are disabled")
            return
        
        try:
            focus = api.getFocusObject()
            if not focus:
                ui.message("No focused control")
                return
            
            word = self._get_word_at_cursor()
            if not word:
                ui.message("No word at cursor")
                return
            
            expansion = self.shortcut_data.get(word)
            if expansion:
                if TextExpander.expand_text_smart(word, expansion):
                    self.last_expanded = (word, expansion)
                    speech.speakText(expansion)
                else:
                    ui.message("Failed to expand shortcut")
            else:
                ui.message(f"'{word}' is not a shortcut")
        
        except Exception as e:
            log.error(f"Error in expandShortcut: {e}")
            ui.message("Error expanding shortcut")
    
    def _get_word_at_cursor(self):
        try:
            focus = api.getFocusObject()
            
            try:
                info = focus.makeTextInfo(textInfos.POSITION_CARET)
                line_info = info.copy()
                line_info.expand(textInfos.UNIT_LINE)
                line_text = line_info.text
                
                caret_pos = info._startOffset - line_info._startOffset
                if caret_pos <= len(line_text):
                    before_caret = line_text[:caret_pos]
                    word_match = re.search(r'\S+$', before_caret)
                    if word_match:
                        return word_match.group()
            except:
                pass
            
            try:
                if hasattr(focus, 'value') and focus.value:
                    val = focus.value
                    word_match = re.search(r'\S+$', val)
                    if word_match:
                        return word_match.group()
            except:
                pass

            try:
                info = focus.makeTextInfo(textInfos.POSITION_CARET)
                info.expand(textInfos.UNIT_WORD)
                word = info.text.strip()
                if word:
                    return word
            except:
                pass
            
            return None
            
        except Exception as e:
            log.debug(f"Word expand failed: {e}")
            return None
    
    @script(
        description="Open keyboard shortcuts manager",
        category="Configuration", 
        gesture="kb:nvda+shift+k"
    )
    def script_openManager(self, gesture):
        def show_dialog():
            try:
                if not wx.IsMainThread():
                    wx.CallAfter(show_dialog)
                    return
                
                for window in wx.GetTopLevelWindows():
                    if isinstance(window, ShortcutManagerDialog):
                        window.Raise()
                        window.SetFocus()
                        return
                
                dlg = ShortcutManagerDialog(gui.mainFrame, self.shortcut_data)
                gui.runScriptModalDialog(dlg)
            
            except Exception as e:
                log.error(f"Error opening manager: {e}")
                ui.message("Error opening shortcuts manager")
        
        wx.CallAfter(show_dialog)
    
    @script(
        description="Enable or disable keyboard shortcuts",
        category="Configuration",
        gesture="kb:nvda+alt+shift+k"
    )
    def script_toggleEnabled(self, gesture):
        enabled = self.shortcut_data.toggle_enabled()
        if enabled:
            ui.message("Keyboard shortcuts enabled")
        else:
            ui.message("Keyboard shortcuts disabled")
    
    @script(
        description="Undo last expansion",
        category="Text Editing",
        gesture="kb:nvda+shift+e"
    )
    def script_undoExpansion(self, gesture):
        if not self.last_expanded:
            ui.message("Nothing to undo")
            return
        
        word, expansion = self.last_expanded
        
        try:
            for _ in range(len(expansion)):
                keyboardHandler.KeyboardInputGesture.fromName("shift+leftArrow").send()
            
            time.sleep(0.05)
            
            old_clip = api.getClipData()
            api.copyToClip(word)
            keyboardHandler.KeyboardInputGesture.fromName("control+v").send()
            
            if old_clip:
                wx.CallLater(100, lambda: api.copyToClip(old_clip))
            
            self.last_expanded = None
            speech.speakText(f"Restored {word}")
        
        except Exception as e:
            log.error(f"Error undoing expansion: {e}")
            ui.message("Failed to undo expansion")
    
    @script(
        description="Show shortcut at cursor",
        category="Text Editing",
        gesture="kb:nvda+shift+s"
    )
    def script_showShortcut(self, gesture):
        word = self._get_word_at_cursor()
        if not word:
            ui.message("No word at cursor")
            return
        
        expansion = self.shortcut_data.get(word)
        if expansion:
            ui.message(f"{word} expands to: {expansion}")
        else:
            ui.message(f"{word} is not a shortcut")
    
    @script(
        description="List all shortcuts",
        category="Configuration",
        gesture="kb:nvda+shift+l"
    )
    def script_listShortcuts(self, gesture):
        shortcuts = self.shortcut_data.get_all()
        if not shortcuts:
            ui.message("No shortcuts defined")
            return
        
        def show_list():
            items = [f"{k}: {v}" for k, v in sorted(shortcuts.items())]
            dlg = wx.SingleChoiceDialog(
                gui.mainFrame,
                "Select a shortcut to hear its expansion:",
                "Shortcuts List",
                items
            )
            
            if dlg.ShowModal() == wx.ID_OK:
                selection = dlg.GetStringSelection()
                ui.message(selection)
            
            dlg.Destroy()
        
        wx.CallAfter(show_list)
    
    def chooseNVDAObjectOverlayClasses(self, obj, clsList):
        if obj.windowClassName in ['Edit', 'RichEdit20', 'RichEdit50W']:
            clsList.insert(0, EnhancedEditField)
    
    def terminate(self):
        log.info("Keyboard Shortcut Autocomplete Professional terminated")
        super(GlobalPlugin, self).terminate()

class EnhancedEditField:
    
    def event_valueChange(self):
        try:
            if hasattr(self, 'value') and self.value:
                words = self.value.split()
                if words:
                    last_word = words[-1]
                    plugin = next((p for p in globalPluginHandler.runningPlugins 
                                   if isinstance(p, GlobalPlugin)), None)
                    if plugin and plugin.shortcut_data.is_enabled():
                        expansion = plugin.shortcut_data.get(last_word)
                        if expansion:
                            queueHandler.queueFunction(
                                queueHandler.eventQueue,
                                ui.message,
                                f"Press NVDA+E to expand to: {expansion[:50]}..."
                            )
        except:
            pass
        
        super().event_valueChange()