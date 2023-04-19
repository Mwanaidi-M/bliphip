from flask import render_template
from bhip import my_db, my_app


@my_app.errorhandler(401)
def error_unauthorized(error):
    return render_template('./error-pages/401-err-pg.html'), 401


@my_app.errorhandler(403)
def error_forbidden(error):
    return render_template('./error-pages/403-err-pg.html'), 403


@my_app.errorhandler(404)
def error_not_found(error):
    return render_template('./error-pages/404-err-pg.html'), 404


@my_app.errorhandler(500)
def error_internal_server(error):
    my_db.session.rollback()
    return render_template('./error-pages/500-err-pg.html'), 500


@my_app.errorhandler(502)
def error_bad_gateway(error):
    my_db.session.rollback()
    return render_template('./error-pages/502-err-pg.html'), 502


@my_app.errorhandler(503)
def error_service_unavailable(error):
    my_db.session.rollback()
    return render_template('./error-pages/503-err-pg.html'), 503


@my_app.errorhandler(504)
def error_gateway_timeout(error):
    return render_template('./error-pages/504-err-pg.html'), 504
