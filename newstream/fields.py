from html import unescape
from django.db import models
from django.utils.encoding import force_str
from django.utils.html import strip_tags

from wagtail.admin.rich_text.editors.draftail import DraftailRichTextArea
from i18nfield.forms import I18nWidget
from i18nfield.fields import I18nFieldMixin


class I18nRichText(I18nWidget):
  """
  The default form widget for I18nRichTextField. It makes use of Django's MultiWidget
  mechanism and does some magic to save you time.
  """
  widget = DraftailRichTextArea


class I18nRichTextField(I18nFieldMixin, models.TextField):
  """
  A RichTextField which takes internationalized data by extending the I18nFieldMixin and using the I18nRichText widget.

  The original wagtail.core.fields.RichTextField is actually editor agnostic, 
  such that you can pass in a different editor for each use of RichTextField in your models.
  But due to the complexity of integrating such agnosticity with the I18nWidget,
  for now I simply use wagtail's default RichText editor widget - DraftailRichTextArea,
  which is assigned in class I18nRichText above.
  """
  widget = I18nRichText