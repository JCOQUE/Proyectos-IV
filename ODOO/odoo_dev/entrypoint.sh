$@

# After starting Odoo, upgrade your module
if [ "$1" = "odoo" ]; then
    echo "Upgrading your module..."
    odoo-bin  -d producer -u pedidos
    odoo -d producer -u pedidos
    ./odoo-bin  -d producer -u pedidos
    ./odoo -d producer -u pedidos
    
fi