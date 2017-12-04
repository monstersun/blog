from . import main
from flask import render_template
from ..deractors import permission_required, admin_required



@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

