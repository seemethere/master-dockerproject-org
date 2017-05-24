#!/usr/bin/env python

import os
import six

import boto3
import bs4 as bs


def human_readable(file_size):
    out = ''
    for count in ['B', 'KB', 'MB', 'GB']:
        if file_size <= 1:
            break
        out = '%3.1f%s' % (file_size, count)
        file_size /= 1024.0
    return out or '{}B'.format(file_size)


if __name__ == '__main__':
    BUCKET_NAME = os.environ.get('BUCKET_NAME', 'master.dockerproject.com')
    s3 = boto3.client('s3')

    front_matter = """\
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
        <title>Docker Master Binaries</title>
        <link rel="stylesheet" href="/static/style.css" />
    </head>
    <body>
        <h1>Docker Master Binaries</h1>
            <div class="wrapper">
                <p>
                These binaries are built from the master branch.
                Want to use that cool new feature that was just merged?
                Download your system's binary below.
                </p>
            <table>
                <thead>
                    <tr>
                        <th><img src="/static/folder.png" alt="[ICO]"/></th>
                        <th>Name</th>
                        <th>Size</th>
                        <th>Uploaded Date</th>
                    </tr>
                </thead>
                <tbody>
    """

    s3_dump = s3.list_objects_v2(Bucket=BUCKET_NAME)
    middle_matter = ''
    for content in s3_dump['Contents']:
        if content['Key'].startswith(('windows', 'linux')):
            middle_matter += """\
            <tr>
                <td valign="top">
                <a href=/{name}><img src=\"/static/{img}.png\" alt=\"[ICO]\">
                </a></td>
                <td><a href=/{name}">{name}</a></td>
                <td>{size}</td>
                <td>{last_modified}</td>
            </tr>
            """.format(
                name=content['Key'],
                img=('text' if content['Key'].endswith(('md5', 'sha256'))
                     else 'default'),
                size=human_readable(content['Size']),
                last_modified=content['LastModified'].isoformat()
            )

    back_matter = """\
                </tbody>
            </table>
        </div>
    </body>
    </html>
    """

    soup = bs.BeautifulSoup(
        front_matter + middle_matter + back_matter,
        'html.parser'
    )

    fake_index = six.StringIO(soup.prettify())
    s3.put_object(
        Bucket=BUCKET_NAME,
        Key='index.html',
        Body=fake_index.read()
    )
