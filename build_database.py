import os
import click
from zipcode_db import ZipCodeDB


def delete_db_file(filename):
  if(os.path.isfile(filename)):
    os.unlink(filename)

def load_zipcodes_file(filename):
    fp = open(filename)
    content = fp.readlines()
    fp.close()
    return content

@click.command()
@click.option('--zipcode-file', default="ceps.txt", help='Filename containing zipcodes.')
@click.option('--output-database', default="./base/cep.db", help='Output database location.')
def build(zipcode_file, output_database):
    click.echo(click.style(f'Building zipcodes database {zipcode_file}', fg='green'))
    # Read zip code file
    content = load_zipcodes_file(zipcode_file)

    # Delete database if exists
    delete_db_file(output_database)

    # Create database
    zipcode_db = ZipCodeDB(output_database, create=True)

    # Populate database
    count = 0
    click.echo(click.style(f'Zip Codes readed {len(content)}', fg='green'))
    with click.progressbar(content) as bar:
        for cep in bar:
            items = cep.split('\t')
            cep = items[0].strip()
            cidade, estado = items[1].split('/')
            cidade = cidade.strip()
            estado = estado.strip()

            if(len(items) >= 3):
                bairro = items[2].strip()
            else:
                bairro = None
            if(len(items) >= 4):
                logradouro = items[3].strip()
            else:
                logradouro = None
            if(len(items) >= 5):
                descricao = items[4].strip()
            else:
                descricao = None
            zipcode_db.insert(cep, cidade, estado, bairro, logradouro, descricao)
            count += 1
    if(len(content) == count):
        click.echo(click.style(f'Zip Codes writed {count}', fg='green'))
    else:
        click.echo(click.style(f'Zip Codes writed {count}', fg='red', bg='yellow'))
    zipcode_db.commit()

if(__name__ == '__main__'):
    build()