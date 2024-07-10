#!/usr/bin/python3

from fabric.api import local
from datetime import datetime
import os

def do_pack():
    """Creates a .tgz archive from the contents of the web_static folder."""
    try:
        # Create versions directory if it doesn't exist
        if not os.path.exists("versions"):
            local("mkdir versions")

        # Generate current time in UTC
        now = datetime.utcnow()

        # Format the archive name web_static_<year><month><day><hour><minute><second>.tgz
        archive_name = "web_static_{}{}{}{}{}{}.tgz".format(
            now.year, now.month, now.day, now.hour, now.minute, now.second)

        # Create the tar command to compress the web_static folder
        command = "tar -cvzf versions/{} web_static".format(archive_name)

        # Execute the command locally
        local(command)

        # Return the path to the created archive
        return "versions/{}".format(archive_name)

    except Exception as e:
        print(e)
        return None

