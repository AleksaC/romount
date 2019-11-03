#!interpreter here

from __future__ import print_function

import re
import sys
import uuid

import inquirer

if sys.version_info[0] < 3:
    import subprocess32 as subprocess
    from commands import getstatusoutput
else:
    import subprocess
    from subprocess import getstatusoutput


def unmounted_partitions():
    lsblk = subprocess.run(['lsblk'], stdout=subprocess.PIPE)

    partitions = filter(
        lambda drive: not drive.startswith('loop'),
        lsblk.stdout.decode('utf-8').splitlines()[1:]
    )
    partitions = filter(
        lambda drive: drive.split()[5] == 'part' and len(drive.split()) <= 6,
        partitions
    )

    unmounted = []
    pattern = re.compile(r'[\W_]+')

    for partition in partitions:
        partition = partition.split()
        unmounted.append(
            "{} - {}".format(pattern.sub('', partition[0]), partition[3])
        )

    return unmounted


def prompt(partitions):
    if len(partitions) == 0:
        print('\nNo unmounted partitions\n')
        exit(0)

    partition = inquirer.prompt([
        inquirer.List(
            'partition',
            message="Which partition to mount?",
            choices=partitions,
            carousel=True
        )
    ])

    if partition is None:
        exit(1)

    return partition['partition'].split()[0]


def mount(partition):
    mount_point = '/media/{}'.format(partition)
    subprocess.run(['sudo', 'mkdir', mount_point], stderr=subprocess.PIPE)

    already_mounted, _ = getstatusoutput('mountpoint {}'.format(mount_point))

    if already_mounted == 0:
        mount_point = '/media/{}'.format(uuid.uuid4().hex)
        subprocess.run(['sudo', 'mkdir', mount_point], stderr=subprocess.PIPE)

    success, message = getstatusoutput(
        'sudo mount -o ro /dev/{} {}'.format(partition, mount_point)
    )

    if success == 0:
        print('Successfully mounted /dev/{} to {}\n'.format(partition, mount_point))
    else:
        print('Something went wrong:')
        print(message, end='\n\n')


def main():
    try:
        mount(prompt(unmounted_partitions()))
    except KeyboardInterrupt:
        print('\nCancelled by user\n')


if __name__ == '__main__':
    main()
