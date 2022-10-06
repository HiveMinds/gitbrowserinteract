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

    #output = subprocess.Popen(bashCommand, shell=True, stdout=subprocess.PIPE).stdout.read()
    p = subprocess.Popen(bashCommand, shell=True,stdout=subprocess.PIPE, bufsize=1)
    lines=[]
    for line in iter(p.stdout.readline, b''):
        print(line)
        lines.append(line)
    p.stdout.close()
    p.wait()
    print("")

    #return output.decode("utf-8")
    return lines


def remove_snap_firefox():
    """TODO: remove this and rely on the bash script instead at Self-host..."""
    output =run_bash_command("yes | sudo snap remove firefox")
    print(f'output0={output}')
    
    # Add firefox ppa to install from apt
    "yes | sudo add-apt-repository ppa:mozillateam/ppa"


def install_apt_firefox():
    # Change the installation priority from snap to ppa.
    change_install_priority="""echo '
Package: *
Pin: release o=LP-PPA-mozillateam
Pin-Priority: 1001
' | sudo tee /etc/apt/preferences.d/mozilla-firefox"""

    

    output1 =run_bash_command(change_install_priority)

    lower_firefox_snap_priority="""echo "
Package: firefox
Pin: version 1:1snap1-0ubuntu2
Pin-Priority: 99
" | sudo tee /etc/apt/preferences"""

    output2 =run_bash_command(lower_firefox_snap_priority)
    print(f'output2={output2}')

    #auto_update_firefox="""echo 'Unattended-Upgrade::Allowed-Origins:: "LP-PPA-mozillateam:${distro_codename}";' | sudo tee /etc/apt/apt.conf.d/51unattended-upgrades-firefox'"""
    auto_update_firefox="""echo 'Unattended-Upgrade::Allowed-Origins:: "LP-PPA-mozillateam:$\{distro_codename\}";' | sudo tee /etc/apt/apt.conf.d/51unattended-upgrades-firefox"""
    #exit()
    output3 =run_bash_command(auto_update_firefox)
    print(f'output3={output3}')
    # TODO: verify file content exists.


    
    #output4 =run_bash_command("sudo add-apt-repository ppa:mozillateam/firefox-next")
    #print(f'output4={output4}')

    output5 =run_bash_command("yes | sudo apt remove firefox")
    print(f'output5={output5}')

    # TODO: verify firefox is not installed.

    # Re-install firefox using apt instead of snap:
    install_firefox="yes | sudo apt install firefox"
    output6 =run_bash_command(install_firefox)
    print(f'output6={output6}')