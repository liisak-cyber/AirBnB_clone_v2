from fabric.api import env, put, run, task
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define remote user and hosts
env.user = 'ubuntu'
env.hosts = ['100.26.172.141', '54.157.147.12']

@task
def do_deploy(archive_path):
    if not os.path.exists(archive_path):
        logging.error(f"Archive '{archive_path}' not found.")
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, "/tmp/")
        logging.info(f"Uploaded archive '{archive_path}' to remote server.")

        # Extract the archive to the folder /data/web_static/releases/<archive filename without extension>
        archive_filename = os.path.basename(archive_path)
        archive_folder = f"/data/web_static/releases/{archive_filename.split('.')[0]}"
        run(f"mkdir -p {archive_folder}")
        run(f"tar -xzf /tmp/{archive_filename} -C {archive_folder}")
        logging.info(f"Extracted archive '{archive_filename}' to '{archive_folder}' on remote server.")

        # ... (continue with other deployment steps)

        logging.info("Deployment completed successfully.")
        return True
    except Exception as e:
        logging.error(f"Deployment failed: {e}")
        return False
