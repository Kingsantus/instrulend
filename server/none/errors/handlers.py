from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(404)
def error_404(error=None):
    return render_template('404.html'), 404

@errors.app_errorhandler(405)
def error_405(error=None):
    return render_template('405.html'), 405

@errors.app_errorhandler(500)
def error_500(error=None):
    return render_template('500.html'), 500

@errors.app_errorhandler(403)
def error_403(error=None):
    return render_template('403.html'), 403
