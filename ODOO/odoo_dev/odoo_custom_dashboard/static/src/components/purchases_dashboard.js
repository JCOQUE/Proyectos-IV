/** @odoo-module */

import { registry } from "@web/core/registry"
import { KpiCard } from "./kpi_card/kpi_card"
import { ChartRenderer } from "./chart_renderer/chart_renderer"
import { useService } from "@web/core/utils/hooks"
import { loadJS } from "@web/core/assets"
import { getColor } from "@web/views/graph/colors"

const { Component, onWillStart, useRef, onMounted, useState } = owl

export class OwlPurchasesDashboard extends Component {
    
    //*Top productos
    async getTopProductos(){
        let domain = [['state','in',['purchase','done']]]

        if (this.state.periodo > 0){
            domain.push(['date_order', '>', this.state.fecha_periodo_actual]);
        }

        const data = await this.orm.readGroup("purchase.report",domain,["product_id","price_total","qty_ordered"],["product_id"],{limit:5,orderby: "price_total desc"})
        this.state.topProductos = {
           data: {
                labels: data.map(d=>d.product_id[1]),
                  datasets: [
                    {
                        label: 'Total Gastado',
                        data: data.map(d => d.price_total),
                        backgroundColor: data.map((_, index) => getColor(index))
                    },
                  {
                    label: 'Cantidad',
                    data: data.map(d=>d.qty_ordered),
                    hoverOffset: 4,
                    backgroundColor: data.map((_,index)=>getColor(index))
                  }]
              },
              domain,
              label_field: 'product_id'
        }
    }
    
    //*Top proveedores
    async getTopProveedores(){
        let domain = [['state','in',['purchase','done']]]

        if (this.state.periodo > 0){
            domain.push(['date_order','>',this.state.fecha_periodo_actual])
        }

        const data = await this.orm.readGroup("purchase.report",domain,["user_id","price_total"],["user_id"],{limit:5,orderby: "price_total desc"})
        this.state.getTopProveedores = {
            data: {
                labels: data.map(d=>d.user_id[1]),
                  datasets: [
                  {
                    label: 'Total',
                    data: data.map(d=>d.price_total),
                    hoverOffset: 4,
                    backgroundColor: data.map((_,index)=>getColor(index))
                }]
              },
              domain,
              label_field: 'user_id'
        }
    }
    
    //*Compras mensuales
    async getComprasMensuales(){
        
        let domain = [['state','in',['sent','draft','purchase','done']]]

        if (this.state.periodo > 0){
            domain.push(['date_order','>',this.state.fecha_periodo_actual])
        }
        
        //*Cogemos la fecha,estado y precio de las ventas agrupados por fecha y estado ordenado por fecha 
        //*El parámetro "lazy" nos permite agrupar por más de un campo 
        const data = await this.orm.readGroup("purchase.report",domain,["date_order","state","price_total"],["date_order","state"],{orderby: "date_order", lazy:false})

        //*Con el operador "Set" evitamos que se repitan campos 
        const labels = [... new Set(data.map(d=>d.date_order))]
        
        const presupuestos = data.filter(d => d.state == 'draft' || d.state == 'sent')
        const ventas = data.filter(d => ['purchase','done'].includes(d.state))

        this.state.comprasMensuales = {
            data: {
                labels:labels,
                  datasets: [
                  {
                    label: 'Presupuestos',
                    data: labels.map(l => presupuestos.filter(q=>l==q.date_order).map(j=>j.price_total).reduce((a,c)=>a+c,0)),
                    hoverOffset: 4,
                    backgroundColor: "red"
                },{
                    label: 'Compras',
                    data: labels.map(l => ventas.filter(q=>l==q.date_order).map(j=>j.price_total).reduce((a,c)=>a+c,0)),
                    hoverOffset: 4,
                    backgroundColor: "green"
                  }]
              },
              domain,
              label_field: 'date_order'
        }
    }

    //*Pedidos por clientes
    async getPedidosClientes(){

        let domain = [['state','in',['sent','draft','purchase','done']]]

        if (this.state.periodo > 0){
            domain.push(['date_order','>',this.state.fecha_periodo_actual])
        }

        const data = await this.orm.readGroup("purchase.report",domain,["partner_id","price_total","qty_ordered"],["partner_id"],{orderby: "partner_id"})

        this.state.pedidosClientes = {
            data: {
                //*Con el operador "Set" evitamos que se repitan campos 
                labels: data.map(d => d.partner_id[1]),
                  datasets: [
                  {
                    label: 'Gastos totales',
                    data: data.map(d=>d.price_total),
                    hoverOffset: 4,
                    backgroundColor: "orange",
                    yAxisID: 'Total',
                    order: 1
                },{
                    label: 'Cantidad pedidos',
                    data: data.map(d=>d.qty_ordered),
                    hoverOffset: 4,
                    backgroundColor: "blue",
                    type: "line",
                    border: "blue",
                    yAxisID: 'Qty',
                    order: 0
                  }]
              },
              scales:{
                    Qty:{
                        position: "right",
                    }
              },
              domain,
              label_field: 'partner_id'
        }
    }

    
    setup(){
        this.state = useState({
            presupuestos:{
                value:20,
                porcentaje:6,
            },
            pedidos:{
                value:20,
                porcentaje:6,
                beneficio:0,
                porcentaje_beneficio: 0
            },
            periodo:90
        })
        this.orm = useService("orm")
        this.actionService = useService("action")

        onWillStart(async () => {
            this.getFecha()
            await this.getPresupuestos()
            await this.getPedidos()
            await this.getTopProductos()
            await this.getTopProveedores()
            await this.getComprasMensuales()
            await this.getPedidosClientes()
        })
    }

    async onChangePeriodo(){
        this.getFecha()
        await this.getPresupuestos()
        await this.getPedidos()
    }
    
    getFecha(){
        //*Cogemos la fecha dependiendo del periodo en el que se encuentre y la formateamos a DD/MM/YYYY
        this.state.fecha_periodo_actual = moment().subtract(this.state.periodo,'days').format("YYYY-MM-DD");
        this.state.fecha_periodo_anterior = moment().subtract(this.state.periodo*2,'days').format("YYYY-MM-DD");
        console.log(this.state.fecha_periodo_anterior,this.state.fecha_periodo_actual)
    }

    async getPresupuestos(){
        //*Recibimos los presupuestos desde la fecha indicada en el filtro

        let domain = [['state','in',['sent','draft']]]

        if (this.state.periodo > 0){
            domain.push(['date_order','>',this.state.fecha_periodo_actual])
        }

        const data = await this.orm.searchCount("purchase.order",domain)
        console.log(data)
        this.state.presupuestos.value = data
        
        let prev_domain = [["state","in",["sent","draft"]]]

        if (this.state.periodo > 0){
            prev_domain.push(["date_order","<=",this.state.fecha_periodo_actual],["date_order",">",this.state.fecha_periodo_anterior])
        }

        const prev_data = await this.orm.searchCount("purchase.order",prev_domain)
        //*Calculamos el porcentaje de pedidos entre los dos últimos periodos
        console.log(prev_data,data)
        const porcentaje = ((data-prev_data)/prev_data)*100
        this.state.presupuestos.porcentaje = porcentaje.toFixed(2)

    }

    async getPedidos(){
        //*Recibimos los presupuestos desde la fecha indicada en el filtro
        let domain = [['state','in',['purchase','done']]]

        if (this.state.periodo > 0){
            domain.push(['date_order','>',this.state.fecha_periodo_actual])
        }

        const data = await this.orm.searchCount("purchase.order",domain)
        
        let prev_domain = [["state","in",['purchase','done']]]

        if (this.state.periodo > 0){
            prev_domain.push(["date_order","<=",this.state.fecha_periodo_actual],["date_order",">",this.state.fecha_periodo_anterior])
        }

        const prev_data = await this.orm.searchCount("purchase.order",prev_domain)
        //*Calculamos el porcentaje de pedidos entre los dos últimos periodos
        const porcentaje = ((data-prev_data)/prev_data)*100
        
        
        //*Calcular el beneficio
        //*Para ello sumaremos la cantidad de los pedidos vendidos en el tiempo indicado
        const beneficio_actual = await this.orm.readGroup("purchase.order",domain,["amount_total:sum"],[])
        const beneficio_anterior = await this.orm.readGroup("purchase.order",prev_domain,["amount_total:sum"],[])
        
        const porcentaje_beneficio = ((beneficio_actual[0].amount_total-beneficio_anterior[0].amount_total)/beneficio_anterior[0].amount_total)*100
        
        //*Calcular el beneficio medio
        //*Para ello calcularemos la media de los pedidos vendidos en el tiempo indicado
        const beneficio_actual_media = await this.orm.readGroup("purchase.order",domain,["amount_total:avg"],[])
        const beneficio_anterior_media = await this.orm.readGroup("purchase.order",prev_domain,["amount_total:avg"],[])
        
        const porcentaje_beneficio_media = ((beneficio_actual_media[0].amount_total-beneficio_anterior_media[0].amount_total)/beneficio_anterior_media[0].amount_total)*100

        this.state.pedidos = {
            value: data,
            porcentaje: porcentaje.toFixed(2),
            beneficio:`$${(beneficio_actual[0].amount_total/1000).toFixed(2)}K`,
            porcentaje_beneficio: porcentaje_beneficio.toFixed(2),
            beneficio_media:`$${(beneficio_actual_media[0].amount_total/1000).toFixed(2)}K`,
            porcentaje_beneficio_media: porcentaje_beneficio_media.toFixed(2)
        }
    }

    async vistaPresupuestos(){

        //*Recibimos los presupuestos desde la fecha indicada en el filtro
        let domain = [["state","in",["sent","draft"]]]

        if (this.state.periodo > 0){
            domain.push(['date_order','>',this.state.fecha_periodo_actual])
        }

        let list_view = await this.orm.searchRead("ir.model.data",[["name","=","view_quotation_tree_with_onboarding"]],["res_id"])

        //*Action para redirigir a la ventana de presupuestos
        this.actionService.doAction({
            type: "ir.actions.act_window",
            name: "Quotations",
            res_model: "purchase.order",
            domain,
            views:[
                [ false, "list"],
                [false,"form"]
            ]
        })

    }

    
    vistaPedidos(){
        
        //*Recibimos los presupuestos desde la fecha indicada en el filtro
        let domain = [['state','in',['purchase','done']]]
        
        if (this.state.periodo > 0){
            domain.push(['date_order','>',this.state.fecha_periodo_actual])
        }
        
        //*Action para redirigir a la ventana de presupuestos
        this.actionService.doAction({
            type: "ir.actions.act_window",
            name: "Quotations",
            res_model: "purchase.order",
            domain,
            context: {group_by: ['date_order']},
            views:[
                [false, "list"],
                [false,"form"]
            ]
        })
        
    }

    async vistaGastos(){
    
        //*Recibimos los presupuestos desde la fecha indicada en el filtro
        let domain = [["state","in",["purchase","done"]]]
    
        if (this.state.periodo > 0){
            domain.push(['date_order','>',this.state.fecha_periodo_actual])
        }
    
        let list_view = await this.orm.searchRead("ir.model.data",[["name","=","view_quotation_tree_with_onboarding"]],["res_id"])
    
        //*Action para redirigir a la ventana de presupuestos
        this.actionService.doAction({
            type: "ir.actions.act_window",
            name: "Quotations",
            res_model: "purchase.order",
            domain,
            views:[
                [false, "pivot"],
                [false,"form"]
            ]
        })
    
    }
}

OwlPurchasesDashboard.template = "owl.OwlPurchasesDashboard"
OwlPurchasesDashboard.components = { KpiCard, ChartRenderer }

registry.category("actions").add("owl.purchases_dashboard", OwlPurchasesDashboard)