"""Prints out an html file to use
"""
import configparser
import duo_web
import os
import argparse


def prepare_args():
    parser = argparse.ArgumentParser(description='DUO Authentication')
    parser.add_argument("--duo_path", default="./duo.conf", type=str)
    return parser.parse_args()


def main(ikey, skey, akey, host):

    username = os.getenv('AUTHENTICATE_UID')

    if username is None:
        raise ValueError("User not authenticated")

    sig_request = duo_web.sign_request(ikey, skey, akey, username)

    out = """
        <!DOCTYPE html>
        <html>
          <head>
            <title>Duo Authentication Prompt</title>
            <meta name='viewport' content='width=device-width, initial-scale=1'>
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <link rel="stylesheet" type="text/css" href="Duo-Frame.css">
          </head>
          <body>
            <h1>Duo Authentication Prompt</h1>
            <script src='/Duo-Web-v2.js'></script>
            <iframe id="duo_iframe"
                    title="Two-Factor Authentication"
                    frameborder="0"
                    data-host="%(host)s"
                    data-sig-request="%(sig_request)s"
                    >
            </iframe>
          </body>
        </html> """ % {
        'host': host,
        'sig_request': sig_request
    }

    with open("test.html", "w") as text_file:
        text_file.write(out)

    print(out)


if __name__ == "__main__":
    args = prepare_args()

    if not os.path.exists(args.duo_path):
        raise ValueError(f"could not find duo conf at {args.duo_path}")

    config = configparser.ConfigParser()

    config.read(args.duo_path)

    main(**dict(config['duo']))
