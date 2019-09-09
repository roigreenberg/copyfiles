import os
import shutil
import wx
from collections import OrderedDict

SMALL = "Small"
BIG = "Big"
DEST = "Dest"


class Folders:
    def __init__(self):
        self.folders = OrderedDict()

    def assign_folder(self, folder, path):
        self.folders[folder] = path

    def get_folder(self, folder):
        return self.folders.get(folder, None)


def do_copy(small_dir, big_dir, dest_dir=None):
    try:
        if not dest_dir:
            dest_dir = os.path.join(small_dir, "big")
        if not os.path.exists(dest_dir):
            os.mkdir(dest_dir)
        for file in os.listdir(small_dir):
            full_file_name = os.path.join(big_dir, file)
            if os.path.isfile(full_file_name):
                shutil.copy(full_file_name, dest_dir)
    except Exception as e:
        return f"Something went wrong: {e}"

    return "Success!"


class MyFrame(wx.Frame):
    def __init__(self, _folders):
        super().__init__(parent=None, title='Hello World')
        self.folders = _folders
        self.folders_ids = OrderedDict()
        self.folders_ids[SMALL] = 1
        self.folders_ids[BIG] = 2
        self.folders_ids[DEST] = 3

        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        for label in self.folders_ids.keys():
            self.sizer.Add(self.add_folder_box(label), 0, wx.ALL | wx.EXPAND, 5)
        my_btn = wx.Button(self.panel, label='Run')
        my_btn.Bind(wx.EVT_BUTTON, self.on_press)
        self.sizer.Add(my_btn, 0, wx.ALL | wx.CENTER, 5)

        self.msg_label = wx.StaticText(self.panel, style=wx.ALIGN_CENTER)
        self.sizer.Add(self.msg_label, 1, wx.ALL, 5)

        self.panel.SetSizer(self.sizer)

        self.Show()
        
    def add_folder_box(self, label):
        text_label = wx.StaticText(self.panel, label=f'{label}:', style=wx.ALIGN_LEFT)

        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(text_label, 0, wx.LEFT, 5)
        text_path = wx.TextCtrl(self.panel, id=1)
        box.Add(text_path, 1, wx.LEFT | wx.EXPAND, 5).SetId(self.folders_ids[label])
        source_btn = wx.Button(self.panel, label='Select')
        source_btn.Bind(wx.EVT_BUTTON, lambda event: self.folder_on_press(event, text_path))
        box.Add(source_btn, 0, wx.RIGHT, 5)

        return box

    def on_press(self, event):
        # source = self.text_source_path.GetValue()
        folders = {}
        for folder, id in self.folders_ids.items():
            value = self.sizer.GetItemById(id, True).GetWindow().GetValue()
            if folder != DEST and (not value or not os.path.isdir(value)):
                self.msg_label.SetLabelText(f"Please enter {folder.lower()} picture folder!")
                return
            else:
                self.folders.assign_folder(folder, value)
        if do_copy(*[self.folders.get_folder(folder) for folder in self.folders_ids.keys()]):
            self.msg_label.SetLabelText(f"Success!")
        else:
            self.msg_label.SetLabelText(f"Something went wrong. please try again.")

    def folder_on_press(self, event, text_path):
        dialog = wx.DirDialog(None, "Choose a directory:", style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if dialog.ShowModal() == wx.ID_OK:
            text_path.SetValue(dialog.GetPath())
            folders.small = dialog.GetPath()
        dialog.Destroy()


if __name__ == '__main__':
    folders = Folders()
    app = wx.App()
    frame = MyFrame(folders)
    app.MainLoop()
    # do_copy(small, big, dest)