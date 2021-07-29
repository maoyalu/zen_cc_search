import click

@click.command()
@click.option(
    '--input_directory',
    '-i',
    help='Location of media file to be converted'
)
def main(input_directory):
    """
        audioConvertor is a command line tool that helps convert
        video files to audio file formats.\n
        example: python cli.py -i input/file/path -o output/path
    """
    click.echo(input_directory)

if __name__ == '__main__':
    main()