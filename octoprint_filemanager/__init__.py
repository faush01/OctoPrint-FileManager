# coding=utf-8
from __future__ import absolute_import

from flask import request, jsonify, make_response, url_for

from octoprint.settings import valid_boolean_trues
from octoprint.filemanager.destinations import FileDestinations
from octoprint.server.util.flask import restricted_access, get_json_command_from_request

import octoprint.plugin


class FilemanagerPlugin(octoprint.plugin.TemplatePlugin,
						octoprint.plugin.AssetPlugin,
						octoprint.plugin.ShutdownPlugin,
						octoprint.plugin.SettingsPlugin):

	def initialize(self):
		pass

	def on_shutdown(self):
		if any(self.workerBusy):
			self._logger.warning("Some workers weren't ready, but OctoPrint got shutdown.")

	def get_assets(self):
		return dict(
			js=["js/jquery.fileDownload.js", "js/ko.single_double_click.js", "js/ko.marquee.js", "js/ko.stopBubble.js", "js/filemanager.js"],
			css=["css/fileManager.css"]
		)

	def get_settings_defaults(self):
		return dict(
			enableCheckboxes=False
		)

	def get_template_configs(self):
		return [
			dict(type="tab", template="filemanager_tab.jinja2", custom_bindings=True),
			dict(type="settings", template="filemanager_settings.jinja2", custom_bindings=False)
		]

	##~~ Softwareupdate hook

	def get_update_information(self):
		# Define the configuration for your plugin to use with the Software Update
		# Plugin here. See https://github.com/foosel/OctoPrint/wiki/Plugin:-Software-Update
		# for details.
		return dict(
			filemanager=dict(
				displayName="FileManager Plugin",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="Salandora",
				repo="OctoPrint-FileManager",
				current=self._plugin_version,

				stable_branch=dict(
					name="Stable",
					branch="master",
					comittish=[
						"master"
					]
				),
				prerelease_branches=[
					dict(
						name="Development",
						branch="devel",
						comittish=[
							"devel",
							"master"
						]
					)
				],

				# update method: pip
				pip="https://github.com/Salandora/OctoPrint-FileManager/archive/{target_version}.zip"
			)
		)


__plugin_name__ = "FileManager"
__plugin_pythoncompat__ = ">=2.7,<4"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = FilemanagerPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}
