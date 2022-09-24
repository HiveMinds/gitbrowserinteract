import subprocess
from typing import List


def run_bash_command(bashCommand):
    """
    :param bashCommand: A string containing a bash command that can be executed.
    """
    # Verbose call.
    # subprocess.Popen(bashCommand, shell=True)
    # Silent call.
    # subprocess.Popen(bashCommand, shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

    # Await completion:
    # Verbose call.
    #proc = subprocess.call(bashCommand, shell=True,stdout=subprocess.PIPE)
    # Silent call.
    #proc = subprocess.call(bashCommand, shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.PIPE)

    # TODO: change from silent call to verbose call that is being waited on.
    output = subprocess.Popen(bashCommand, shell=True, stdout=subprocess.PIPE).stdout.read()
    
    return output.decode("utf-8")


def remove_snap_firefox():
    output =run_bash_command("yes | sudo snap remove firefox")
    "yes | sudo add-apt-repository ppa:mozillateam/ppa"

    #echo '
    #Package: *
    #Pin: release o=LP-PPA-mozillateam
    #Pin-Priority: 1001
    #' | sudo tee /etc/apt/preferences.d/mozilla-firefox

    #echo 'Unattended-Upgrade::Allowed-Origins:: "LP-PPA-mozillateam:${distro_codename}";' | sudo tee /etc/apt/apt.conf.d/51unattended-upgrades-firefox

    # TODO: verify firefox is not installed.

    # Re-install firefox using apt instead of snap:
    # sudo apt install firefox