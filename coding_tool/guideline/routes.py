from flask import Blueprint, render_template
from coding_tool.models import Publication, Guideline

import numpy as np

guideline = Blueprint('guideline', __name__)


@guideline.route("/guidelines")
def all():
    guidelines = Guideline.query.all()
    return render_template('guidelines.html', guidelines=guidelines)


@guideline.route("/guideline/<int:guide_id>/")
def guide(guide_id):
    guideline = Guideline.query.get_or_404(guide_id)
    return render_template('guideline_details.html', guideline=guideline)
