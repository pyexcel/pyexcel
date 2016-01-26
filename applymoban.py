from os import path, system

config_dir = 'commons/config'
template_dir = 'commons/templates'

if not path.exists("commons"):
    system("git clone https://github.com/pyexcel/pyexcel-commons.git commons")
system("moban -cd {0} -td {1} .moban.d -t docs/source/conf.py -o doc/source/conf.py -c moban.yaml".format(config_dir, template_dir))
system("moban -cd {0} -td {1} .moban.d -t setup.py -o setup.py -c moban.yaml".format(config_dir, template_dir))
system("moban -cd {0} -td {1} .moban.d -t travis.yml -o .travis.yml -c moban.yaml".format(config_dir, template_dir))
system("moban -cd {0} -td {1} -t LICENSE.jj2 -o LICENSE -c moban.yaml".format(config_dir, template_dir))
system("moban -cd {0} -td {1} .moban.d -t tests/requirements.txt -o tests/requirements.txt -c moban.yaml".format(config_dir, template_dir))
system("moban -cd {0} -td {1} .moban.d -t MANIFEST.in.jj2 -o MANIFEST.in -c moban.yaml".format(config_dir, template_dir))
