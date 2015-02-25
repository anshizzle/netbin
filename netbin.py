import click


@click.command()
@click.option('--count', default=1, help='Number of greetings.')
@click.option('--name', prompt='Your name',
              help='The person to greet.')

def netbin(count, name):
	for x in range(count):
		click.echo('Hello %s!' % name)


if __name__ == '__main__':
    netbin()