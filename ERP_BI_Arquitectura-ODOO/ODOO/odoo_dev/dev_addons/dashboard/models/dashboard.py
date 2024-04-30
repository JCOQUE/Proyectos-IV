from odoo import models, api
import logging

class CustomBoard(models.Model):
    _logger = logging.getLogger(__name__)
    _inherit = 'board.board'  # Asegúrate de que 'board.board' sea el modelo correcto

    @api.model
    def add_to_dashboard(self, *args, **kwargs):
        self._logger.info("Añadiendo al tablero personalizado...")
        # Tu lógica personalizada aquí
        result = super(CustomBoard, self).add_to_dashboard(*args, **kwargs)
        return result
 