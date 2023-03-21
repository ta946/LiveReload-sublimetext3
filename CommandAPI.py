#!/usr/bin/python
# -*- coding: utf-8 -*-

import sublime
import sublime_plugin
import LiveReload
import webbrowser
import os


class LiveReloadTest(sublime_plugin.ApplicationCommand):

    def run(self):
        path = os.path.join(sublime.packages_path(), 'LiveReload', 'web')
        file_name = os.path.join(path, 'test.html')
        webbrowser.open_new_tab("file://"+file_name)


class LiveReloadHelp(sublime_plugin.ApplicationCommand):

    def run(self):
        webbrowser.open_new_tab('https://github.com/alepez/LiveReload-sublimetext3#using'
                                )


class LiveReloadEnablePluginCommand(sublime_plugin.ApplicationCommand):

    def on_done(self, index):
        if index != -1:
            LiveReload.Plugin.togglePlugin(index)

    def run(self):
        sublime.active_window().show_quick_panel(LiveReload.Plugin.listPlugins(),
                self.on_done)


class LiveReloadEnablePluginByNameCommand(sublime_plugin.ApplicationCommand):

    def run(self, name, enable=None):
        mcs = LiveReload.Plugin
        try:
            plugin = mcs.getPlugin(name)
            index = mcs.plugins.index(plugin.__class__)
        except:
            sublime.error_message('LiveReload plugin {} not found!'.format(name))
            return
        if enable is None:
            mcs.togglePlugin(index)
        elif enable:
            if plugin.isEnabled:
                return
            mcs.enabled_plugins.append(plugin.name)
            sublime.set_timeout(lambda : \
                                sublime.status_message('"%s" the LiveReload plug-in has been enabled!'
                                 % plugin.title), 100)
            plugin.onEnabled()
        elif not enable:
            if not plugin.isEnabled:
                return
            mcs.enabled_plugins.remove(plugin.name)
            sublime.set_timeout(lambda : \
                                sublime.status_message('"%s" the LiveReload plug-in has been disabled!'
                                 % plugin.title), 100)
            plugin.onDisabled()
