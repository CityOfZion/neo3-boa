import os
import shutil
import subprocess
import sys

docs_dir = os.path.abspath(f'{__file__}/..')
latex_build_dir = os.sep.join([docs_dir, 'build', 'latex'])
if os.path.isdir(latex_build_dir):
    shutil.rmtree(latex_build_dir)

ext = '.bat' if sys.platform.startswith('win') else ''
os.system(f'{docs_dir}{os.sep}make{ext} latex')

args = f'{latex_build_dir}{os.sep}make{ext} all-pdf'.split(' ')

process = subprocess.Popen(args,
                           stdin=subprocess.PIPE,
                           stderr=subprocess.STDOUT,
                           text=True)
process.communicate(input='R')

for _ in range(2):
    # need to rerun some times to make sure all the information is included
    # it's a latexpdf limitation
    process = subprocess.Popen(args,
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               text=True)
    process.communicate(input='R')

output_pdf = os.sep.join([latex_build_dir, 'neo3-boa.pdf'])
if not os.path.isfile(output_pdf):
    raise ValueError


project_root = os.path.abspath(f'{docs_dir}/..')
is_in_path = project_root in sys.path
if is_in_path:
    import boa3
    current_version = boa3.__version__
else:
    sys.path.append(project_root)
    import boa3
    current_version = boa3.__version__
    sys.path.pop()

expected_output_file = os.sep.join([docs_dir, 'versions', f'neo3-boa_{current_version}_documentation.pdf'])
shutil.copy(output_pdf, expected_output_file)

common_path = os.path.commonpath([os.path.abspath('.'), expected_output_file])
print(f'\nDocumentation saved on {expected_output_file.removeprefix(common_path)}')
