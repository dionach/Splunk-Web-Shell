Splunk WebShell
================

Now and then, while performing internal penetration tests we come across Splunk default installs where uncredentialed access to anyone with access to the system is allowed, logging them as the "admin" user and therefore granting them administrative access to the management panel.

This project contains a web shell specifically developed for Splunk. In order to deploy the shell you have to log into the admin panel, browse to "Manage Apps", and once there click on "Install app from file", select the "webShell.tar.gz" file, and follow the instructions.

Please, note that as it is configured at the moment, the app requires access to the admin panel first, this was done on purpose to avoid random access to the web shell, but this is easy modifiable in the source code if the situation requires it.
