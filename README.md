# SDA_backup_cleanup
This script is used to call Cisco Catalyst Center API to delete backups.
It first list all backups, keep the latest number of backups set by retention, delete all other older backups.
You can set variable retention to the number of backups you want to keep.
Pythom module requests is required.
To run this script:
Set the Catalyst Center host ip address, username, password
set the retention (default is 4)
