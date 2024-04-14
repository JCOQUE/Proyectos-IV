/** @odoo-module */

import { registry } from "@web/core/registry"
import { loadJS } from "@web/core/assets"
const { Component, onWillStart, useRef, onMounted } = owl
import { useService } from "@web/core/utils/hooks"

export class ChartRenderer extends Component {
    setup(){
        this.chartRef = useRef("chart")
        this.actionService = useService("action")


        onWillStart(async ()=>{
            await loadJS("https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js")
        })

        onMounted(()=>this.renderChart())
    }

    renderChart(){
        new Chart(this.chartRef.el,
        {
          type: this.props.type,
          data: this.props.config.data,
          options: {
            onClick: (e) => {
              //*Cogemos el elemento pulsado y obtenemos su etiqueta
              const active = e.chart.getActiveElements()

              if (active.length > 0) {
                const label = e.chart.data.labels[active[0].index]
                const dataset = e.chart.data.datasets[active[0].datasetIndex]

                const { label_field, domain } = this.props.config
                
                //* Comprábamos si hemos recibido el dominio 
                let new_domain = domain ? domain : []

                //*Si tenemos el campo para seleccionar lo añadimos para la búsqueda
                if (label_field){
                  //* Si hemos seleccionado una fecha debemos formatearla correctamente para la búsqueda
                  if(label_field.includes("date")){

                    const timeStamp = Date.parse(label)
                    const mes_seleccionado = moment(label, "MMMM YYYY");
                    const mes_inicial = mes_seleccionado.format("YYYY-MM-DD")
                    const mes_final = mes_seleccionado.endOf('month').format("YYYY-MM-DD")
                    
                    let date_field = this.props.model === "purchase.report" ? 'date_order' : 'date';
                    new_domain.push([date_field, '>=', mes_inicial], [date_field, '<=', mes_final]);


                  }else{
                    new_domain.push([label_field,"=",label])
                  }
                  
                }

                if (dataset.label == "Presupuestos"){
                    new_domain.push(['state','in',['draft','sent']])
                } 

                if (dataset.label == "Ventas"){
                    new_domain.push(['state','in',['sale','done']])
                } 

                this.actionService.doAction({
                  type: "ir.actions.act_window",
                  name: this.props.title,
                  res_model: this.props.model,
                  domain: new_domain,
                  views: [
                      [false,"list"],
                      [false,"form"]
                  ]

                })
              }

            },
            responsive: true,
            plugins: {
              legend: {
                position: 'bottom',
              },
              title: {
                display: true,
                text: this.props.title,
                position: 'bottom',
              }
            },
            //* Cargamos las escalas definidas en la función si existen
            scales: 'scales' in this.props.config ? this.props.config.scales : {}
          },
        }
      );
    }
}

ChartRenderer.template = "owl.ChartRenderer"