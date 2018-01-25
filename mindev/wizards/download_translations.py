# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (c) 2011-TODAY MINORISA (http://www.minorisa.net)
#                             All Rights Reserved.
#                             Minorisa <contact@minorisa.net>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import cStringIO
import contextlib
# import ConfigParser
import os
# import polib
# import git

from openerp import models, fields, api
from openerp import tools
from openerp.exceptions import ValidationError
from openerp.modules import module as omm
# from openerp.tools.translate import TinyPoFile


class DownloadTranslations(models.TransientModel):
    _name = 'mindev.download.translation'
    _description = 'MinDev Download Translations'

    module = fields.Many2one('ir.module.module', string="Module",
                             domain=[('state', '=', 'installed')])
    languages = fields.Many2many('res.lang', string="Languages")
    i18n_path = fields.Char(string="i18n Path")
    git_repo = fields.Char(string="Git Repo")
    has_git = fields.Boolean(string="Has Git")
    do_commit = fields.Boolean(string="Do Commit & Push")
    state = fields.Selection(selection=[
        ('start', 'start'),
        ('end', 'end'),
    ], string="State", required=True, default='start')
    html_res = fields.Html(string="Result")

    @api.model
    def default_get(self, fields_list):
        res = super(DownloadTranslations, self).default_get(fields_list=fields_list)
        lang_en = self.env.ref('base.lang_en')
        lang_en_id = lang_en and lang_en.id or False
        res.update({
            'languages': [
                (4, x.id) for x in self.env['res.lang'].search([]) if x.id != lang_en_id
            ]
        })
        return res

    @api.onchange('module')
    def onchange_module(self):
        i18n_path = False
        has_git = False
        git_repo = False

        if self.module:
            trav = omm.get_module_path(self.module.name)
            i18n_path = os.path.join(trav, 'i18n')
            while trav != '/':
                if os.path.exists(os.path.join(trav, '.git')):
                    git_repo = trav
                    has_git = True
                    break
                trav = os.path.dirname(trav)

        self.i18n_path = i18n_path
        self.has_git = has_git
        self.git_repo = git_repo
        self.do_commit = has_git

    @api.multi
    def do_download(self):
        self.ensure_one()
        if not self.module:
            raise ValidationError("You must select a module!")

        # Get again the path because this field is readonly and is not updated by onchange
        i18n_path = self.i18n_path
        # project_path = omm.get_module_resource(self.module.name, 'i18n')
        if not i18n_path:
            raise ValidationError("Unable to create i18n path!")

        # Check if i18n path exists; if not, create it
        if not os.path.exists(i18n_path):
            os.makedirs(i18n_path)

        i18n_files = []
        # Create .po file for each language
        for lang in self.languages:
            name = u"{}.po".format(lang.iso_code)
            i18n_file = os.path.join(i18n_path, name)
            # i18n_file = os.path.join('/home/jaume.planas/Escriptori', name)
            try:
                with contextlib.closing(cStringIO.StringIO()) as buf:
                    # TODO Rewrite trans_export?
                    tools.trans_export(lang.code, [self.module.name], buf, 'po', self._cr)
                    buf.seek(0)
                    last_msgid = False
                    with open(i18n_file, 'w') as output:
                        for line in buf:
                            # if line[:5] == "msgid":
                            #     last_msgid = line[6:]
                            # if line[:6] == "msgstr":
                            #     if last_msgid == line[7:]:
                            #         line = "msgstr \"\""
                            #     last_msgid = False
                            output.write(line)
            except Exception:
                raise
            i18n_files.append(i18n_file)

        res = """
<h2>The following PO files have been created or modified</h2>
<ul>
        """
        for x in i18n_files:
            res += """
    <li>{}</li>
            """.format(x)
        res += """
</ul>
        """
#         if self.do_commit:
#             repo_name = self.git_repo
#             repo = git.Repo(repo_name)
#             relative_path = os.path.relpath(i18n_path, repo_name)
#             files = [
#                 x.a_path for x in repo.index.diff(None, paths=[
#                     relative_path
#                 ])
#             ]
#             xgit = repo.git
#             xgit.add(files)
#             git_msg = u"[TRA]][{}] PO files exported from Odoo".format(self.module.name)
#             xgit.commit('-m', git_msg, files)
#             commit = repo.head.commit
#             branch = repo.head.ref.name
#             hexsha = commit.hexsha
#             xgit.push('origin', '{}:{}'.format(hexsha, branch))
#
#             res += """
# <h2>The following commit has been created</h2>
# <pre>
#             """
#             res += xgit.show('--name-only', hexsha)
#             res += """
# </pre>
#             """
        self.html_res = res
        self.state = 'end'
        return {
            'type': 'ir.actions.act_window',
            'name': 'Download Translation Results',
            'res_model': 'mindev.download.translation',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'views': [(False, 'form')],
            'target': 'new',
        }
