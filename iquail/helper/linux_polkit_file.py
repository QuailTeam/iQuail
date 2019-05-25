import os

polkit_file ="""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE policyconfig PUBLIC "-//freedesktop//DTD PolicyKit Policy Configuration 1.0//EN"
"http://www.freedesktop.org/standards/PolicyKit/1.0/policyconfig.dtd">
<policyconfig>
<action id="%s">
<message gettext-domain="%s">%s</message>
<defaults>
<allow_any>auth_admin_keep</allow_any>
<allow_inactive>auth_admin_keep</allow_inactive>
<allow_active>auth_admin_keep</allow_active>
</defaults>
<annotate key="org.freedesktop.policykit.exec.path">%s</annotate>
<annotate key ="org.freedesktop.policykit.exec.allow_gui">true</annotate>
</action>
</policyconfig>"""


def polkit_get_file(bin_path, action='iQuail', domain='iQuail', txt_msg='Authentication required to run iQuail'):
    return polkit_file % (action, domain, txt_msg, bin_path)


def polkit_get_file_name(uid):
    return os.path.join('/usr', 'share', 'polkit-1', 'actions', uid) + '.policy'


def polkit_check(uid):
    return os.path.isfile(polkit_get_file_name(uid))


def polkit_install(bin_path, uid, file=None):
    if file is None:
        file = polkit_get_file(bin_path)
    polkit = open(polkit_get_file_name(uid), 'w+')
    polkit.write(file)
    polkit.close()


def polkit_remove(uid):
    os.remove(polkit_get_file_name(uid))


def polkit_get_file_name(uid):
    return os.path.join('/usr', 'share', 'polkit-1', 'actions', uid) + '.policy'

