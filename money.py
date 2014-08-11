import os
import sys
from docopt import docopt
from textwrap import dedent
import pickle

db_filename = 'db.dat'
db_version = '0.1.001'
db = None

def init():
  db = {'version': db_version,
        'accounts': {},
        'transactions': None
       }
  return db

def check(db):
  version = db['version']
  if version != db_version:
    print('You need to update your databse')

main_doc = """
Usage:
  money account create <name> [(<initial> <currency>)]
  money account list
  money account info <name>
  money account delete <name>
"""

class Account:

  def __init__(self, name, initial = 0.0, currency = 'dollar'):
    self.name = name
    self.initial = initial
    self.current = 0.0
    self.currency = currency

  def __unicode__(self):
    return 'Account "%s" contains %d %s' %(self.name, self.current, self.currency)

  def __str__(self):
    return self.__unicode__()

  @staticmethod
  def get_accounts():
    global db
    return db['accounts']

  @staticmethod
  def create(name, initial_amount, currency):
    accounts = Account.get_accounts()
    accounts[name] = Account(name, initial_amount, currency)
    return accounts[name]

  @staticmethod
  def list(args):
    accounts = Account.get_accounts()
    for account_name in accounts:
      print(account_name)

  @staticmethod
  def info(name):
    accounts = Account.get_accounts()
    if name not in accounts:
      print('wrong name')
      sys.exit(-1)
    account = accounts[name]
    print(account)


def main():
  args = docopt(main_doc, help = True, options_first = True)
  print(args)

  if os.path.exists(db_filename):
    db = pickle.load(open(db_filename, 'rb'))
    if check(db) == False:
      sys.exit(1)
  else:
    db = init()

  import pdb; pdb.set_trace()

  if args['account']:
    command = 'create' if args['create'] else 'list' if args['list'] else 'info' if args['info'] else 'delete' if args['delete'] else 'unknown'
    if hasattr(Account, command):
      cmd = getattr(Account, command)
      cmd(args)

    accounts = db['accounts']
    if args['new']:
      name = args['<name>']
      initial = float(args['<initial>']) if args['<initial>'] else 0.0
      currency = args['<currency>'] if args['<currency>'] else 'dollar'
      account = Account(name, initial, currency)
      accounts[name] = account
    elif args['list']:
      for account_name in accounts:
        print(account_name)
    elif args['info']:
      name = args['<name>']
      if name not in accounts:
        print('wrong name')
        sys.exit(-1)
      account = accounts[name]
      print(account)

  pickle.dump(db, open(db_filename, 'wb'))

if __name__ == '__main__':
  main()
