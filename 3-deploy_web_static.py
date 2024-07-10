#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to your web servers using the function deploy.
"""

from fabric.api import env, local, put, run
import os
from datetime import datetime

# Define remote user and hosts
env.user = 'ubuntu'
env.hosts = ['100.26.172.141', '54.157.147.12']

def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.
    """
    try:
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = "versions/web_static_{}.tgz".format(now)
        local("mkdir -p versions")
        local("tar -cvzf {} web_static".format(archive_path))
        return archive_path
    except Exception:
        return None

def do_deploy(archive_path):
    """
    Distributes an archive to your web servers
    """
    if not os.path.exists(archive_path):
        print(f"Archive file '{archive_path}' not found.")
        return False
    
    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, "/tmp/")
        
        # Extract the archive to the folder /data/web_static/releases/<archive filename without extension>
        archive_filename = os.path.basename(archive_path)
        archive_folder = "/data/web_static/releases/{}".format(
            archive_filename.split('.')[0])
        
        run("mkdir -p {}".format(archive_folder))
        run("tar -xzf /tmp/{} -C {}".format(archive_filename, archive_folder))
        
        # Remove the archive from the web server
        run("rm /tmp/{}".format(archive_filename))
        
        # Move contents from extracted folder to its parent folder
        run("mv {}/web_static/* {}".format(archive_folder, archive_folder))
        
        # Remove the extracted folder
        run("rm -rf {}/web_static".format(archive_folder))
        
        # Remove the symbolic link /data/web_static/current from the web server
        run("rm -rf /data/web_static/current")
        
        # Create a new symbolic link /data/web_static/current linked to the new version of your code
        run("ln -s {} /data/web_static/current".format(archive_folder))
        
        print("New version deployed!")
        return True
    
    except Exception as e:
        print(e)
        return False

def deploy():
    """
    Full deployment: Packs the web_static folder and deploys the archive to web servers.
    """
    archive_path = do_pack()
    if not archive_path:
        return False
    
    return do_deploy(archive_path)
