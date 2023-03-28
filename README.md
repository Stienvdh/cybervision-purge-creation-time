# Cisco Cyber Vision: Purge components by creation time

This collection of scripts allows to (1) consult the amount of devices created in Cyber Vision per creation time, (2) select a date for which to purge all new components in the Cyber Vision database, and (3) execute that purge. The IP addresses of the components to be purged will be listed in an Excel file generated after step (2), at which point the user can add or delete certain IP addresses that will be added, respectively deleted from the purge executed in step (3). 

![](workflow.png)

## Installation

1. Log in to your Cyber Vision Center CLI (default username = `cv-admin`)

2. Change to be a root user by ussuing the `sudo -i` command

3. Change your working directory using `/data/home/cv-admin`

4. Create a new file called `collect_scanned_components.py` and copy the contents from the same file in this repository

5. Create a new file called `purge_scanned_components.py` and copy the contents from the same file in this repository

## Usage

1. Log in to your Cyber Vision Center CLI (default username = `cv-admin`)

2. Change to be a root user by ussuing the `sudo -i` command

3. Change your working directory using `/data/home/cv-admin`

4. Run step (1) by running the command `python3 collect_scanned_components.py` 

5. From the prompt given by the script, consult the amount of devices generated at the listed creation times

6. Copy the creation time for which you want to delete new components, and paste it back to the prompt when asked for it (`Copy creation time to delete components for: `)

7. Press Enter

8. Now, you can consult/modify the list of IP addresses to purge in `/data/home/cv-admin/ip_addresses_to_purge.csv`

9. Purge the selected devices by running `python3 purge_scanned_components.py` 