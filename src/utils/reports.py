import pandas as pd 
from django.db import DatabaseError, transaction
from django.db.models import Count
from items.models import Activo
from proveedores.models import Proveedor
from operaciones.models import MANTENIMIENTO_CHOICES, Operacion
from pivottablejs import pivot_ui

from bokeh.models import ColumnDataSource
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn
from bokeh.io import output_file, show

idx = pd.IndexSlice

import math



def getActivos(save):
    savePath = '/Users/juanjosebonilla/Desktop/Trabajo/Mantenimiento/ReporteMantenimientoDj.xlsx'
    writer = pd.ExcelWriter(savePath)
    gastos = {'totalCost':'CONSOLIDADO','totalCorCost':'correctivo','totalPrevCost':'preventivo'}
    frames = []
    for nombre , gasto in gastos.items():
        if gasto == 'CONSOLIDADO':
            #activos = Activo.objects.filter(operacions__timestamp__year__gte = 2018)
            activos = Activo.objects.distinct().annotate(op_num=Count('operacion')).filter(op_num__gt=0)#.filter(operacion__timestamp__year =2018).filter(operacion__timestamp__month=12)
        else :
            activos = Activo.objects.distinct().filter(operacion__mantenimiento = gasto)#.filter(operacion__timestamp__year =2018).filter(operacion__timestamp__month=12)

        #fields = ['local','ubicacion2','nombre',nombre,'marca','modelo','placa','num_cor','num_prev'] 
        fields = ['pdv','ubicacion','descripcion',nombre,'marca','modelo','placa','num_cor','num_prev']
        if len(activos) > 0:
            conGastoDf = pd.DataFrame([{fn:getattr(f,fn) for fn in fields} for f in activos])
            print(conGastoDf)
            
                ##Tabla Dinamica

            gastoSource = conGastoDf.copy(deep= True)
            gastoSource.reset_index(inplace = True)
            gastoSource['Total PDV'] =  0
            gastoSource['Total ubicacion'] = 0
            for local in gastoSource['pdv'].unique():
                mask = gastoSource['pdv'] == local
                suma = gastoSource[mask][nombre].sum()
                gastoSource.loc[mask,'Total PDV'] = suma

            for ubicacion in gastoSource['ubicacion'].unique():
                for local in gastoSource['pdv'].unique():
                    mask = (gastoSource['ubicacion'] == ubicacion) & (gastoSource['pdv'] == local)
                    suma = gastoSource[mask][nombre].sum()
                    gastoSource.loc[mask,'Total ubicacion'] = suma


            total = gastoSource[nombre].sum()

            values = {'Total PDV':[total],'pdv':['Gran Total']}
            row = pd.DataFrame.from_dict(values)
            gastoSource.sort_values(['Total PDV','Total ubicacion',nombre], ascending= False, inplace = True)
            gastoSource = gastoSource.append(row,ignore_index=True)
            #gastoSource = gastoSource.groupby(['Total PDV','local','Total ubicacion','ubicacion2'])
            gastoSource.set_index(['Total PDV','pdv','Total ubicacion','ubicacion'],inplace = True)
            #gastoSource.drop(gastoSource.columns[[0]],axis = 1,inplace = True)
            col_list = ['descripcion', 'placa','marca','modelo', nombre,'num_cor', 'num_prev']
            #col_list = ['nombre', 'placa', nombre,'num_cor', 'num_prev']
            gastoSource = gastoSource.reindex(columns=col_list)
            #print(gastoSource.columns)
            gastoSource.to_excel(writer,sheet_name=nombre)
            frames.append(gastoSource)
            #print(gastoSource)

    if save :
        writer.save()
    writer.close()
    return frames

def getActivos2(save,month,year):
    savePath = '/Users/juanjosebonilla/Desktop/Trabajo/Mantenimiento/ReporteMantenimientoDj.xlsx'
    writer = pd.ExcelWriter(savePath)
    gastos = {'gettotalCost':'CONSOLIDADO','getCorCost':'correctivo','getPrevCost':'preventivo'}
    frames = []
    for nombre , gasto in gastos.items():
        if gasto == 'CONSOLIDADO':
            #activos = Activo.objects.filter(operacions__timestamp__year__gte = 2018)
            activos = Activo.objects.distinct().annotate(op_num=Count('operacion')).filter(op_num__gt=0).filter(operacion__timestamp__year =2018).filter(operacion__timestamp__month=12)
        else :
            activos = Activo.objects.distinct().filter(operacion__mantenimiento = gasto).filter(operacion__timestamp__year =2018).filter(operacion__timestamp__month=12)

        #fields = ['local','ubicacion2','nombre',nombre,'marca','modelo','placa','num_cor','num_prev'] 
        #fields = ['pdv','ubicacion','descripcion',nombre,'marca','modelo','placa','num_cor','num_prev']
        fields = ['pdv','ubicacion','descripcion','marca','modelo','placa']
        if len(activos) > 0:
            conGastoDf = pd.DataFrame([{fn:getattr(f,fn) for fn in fields} for f in activos])
            print('first try',conGastoDf)
            ## agregar tres columnas []
            conGastoDf[nombre] = 0
            conGastoDf['num_cor'] = 0
            conGastoDf['num_prev'] = 0
            for index, row in conGastoDf.iterrows():
                method_to_call = getattr(activos[index], nombre)
                countCor = getattr(activos[index],'getCorCount')
                countPre = getattr(activos[index],'getPrevCount')
                conGastoDf.loc[index,nombre] = method_to_call(month,year)
                conGastoDf.loc[index,'num_cor'] = countCor(month,year)
                conGastoDf.loc[index,'num_prev'] = countPre(month,year)


                print(row)
               

            
                ##Tabla Dinamica

            gastoSource = conGastoDf.copy(deep= True)
            print('first frame')
            print(gastoSource)
            gastoSource.reset_index(inplace = True)
            gastoSource['Total PDV'] =  0
            gastoSource['Total ubicacion'] = 0
            for local in gastoSource['pdv'].unique():
                mask = gastoSource['pdv'] == local
                suma = gastoSource[mask][nombre].sum()
                gastoSource.loc[mask,'Total PDV'] = suma

            for ubicacion in gastoSource['ubicacion'].unique():
                for local in gastoSource['pdv'].unique():
                    mask = (gastoSource['ubicacion'] == ubicacion) & (gastoSource['pdv'] == local)
                    suma = gastoSource[mask][nombre].sum()
                    gastoSource.loc[mask,'Total ubicacion'] = suma


            total = gastoSource[nombre].sum()

            values = {'Total PDV':[total],'pdv':['Gran Total']}
            row = pd.DataFrame.from_dict(values)
            gastoSource.sort_values(['Total PDV','Total ubicacion',nombre], ascending= False, inplace = True)
            gastoSource = gastoSource.append(row,ignore_index=True)
            #gastoSource = gastoSource.groupby(['Total PDV','local','Total ubicacion','ubicacion2'])
            gastoSource.set_index(['Total PDV','pdv','Total ubicacion','ubicacion'],inplace = True)
            #gastoSource.drop(gastoSource.columns[[0]],axis = 1,inplace = True)
            col_list = ['descripcion', 'placa','marca','modelo', nombre,'num_cor', 'num_prev']
            #col_list = ['nombre', 'placa', nombre,'num_cor', 'num_prev']
            gastoSource = gastoSource.reindex(columns=col_list)
            #print(gastoSource.columns)
            gastoSource.to_excel(writer,sheet_name=nombre)
            frames.append(gastoSource)
            #print(gastoSource)

    if save :
        writer.save()
    writer.close()
    return frames




def helperSpan(currentList, entries):
    for index, entry in enumerate(entries):
        columnDic = currentList[index]
        print('type',type(entry),' entry: ',entry)
        if isinstance(entry,float) and math.isnan(entry):
            entry = " "
        if entry in columnDic:
            columnDic[entry] = columnDic[entry] + 1
        else:
            columnDic[entry] = 0 


    



def genPivotHtml():
    DF = getActivos(False)[0]
    #DF.reset_index(inplace=True)
    #cols = ['totalCost','num_cor','num_prev','Total ubicacion']
    #DF[cols] = DF[cols].apply(pd.to_numeric, errors='coerce')
    #DF[cols] = DF[cols].fillna(0)
    print(DF.info())
    print(DF)


    ## clean df

    # with pivotTablejs
   #pivot_ui(df)
    #output = df.to_html()
    #print(output)

    ##Bokeh

    # Columns = [TableColumn(field=Ci, title=Ci) for Ci in DF.columns] # bokeh columns
    # data_table = DataTable(columns=Columns, source=ColumnDataSource(DF)) # bokeh table
    # show(data_table)

    #Style tag

    styles = '<style> table,th,td { border: 1px solid black;}</style>'

    ## Custom html

    #html = '<html>' + '<head>' + styles + '</head>' + <'body>' '<table>'
    html = '<table class="table table-bordered">'

    ## generate table columns
    columns = []
    indexValues = DF.index.values
    index = ['Total PDV' , 'pdv','Total ubicacion','ubicacion']
    cols = DF.columns
    columns.extend(index)
    columns.extend(cols)
    columnRow = '<tr>'

    for col in columns :
        columnRow = columnRow + '<th>' + col + '</th>'
    columnRow = columnRow + '</tr>'

    html = html + columnRow

    entries = [{},{},{},{}]

    # for index , row in DF.iterrows():
    #     #print('Current index',index)
    #     #print('pdv' , index[1])
    #     helperSpan(entries,index)
    # print(entries)

    total_pdv = 1
    pdv = 1
    total_ub = 1
    print(DF)

    for index , row in DF.iterrows():
        #print('type :', type(index[0]))
        print(index)

        html_row = '<tr>'

        index_L = 0
        if not math.isnan(index[2]):
            #index_L =  len(DF.loc[idx[index[0],index[1],index[2],index[3]],:])
            if total_pdv == 1:
                total_pdv = len(DF.loc[idx[index[0],:,:,:],:])
                print('starting total Pdv with row_span: ' + str(total_pdv))
                column = '<td rowspan="' + str(total_pdv) + '">' + str(index[0]) + '</td>'
                html_row = html_row + column
            else:
                total_pdv = total_pdv - 1
            
            if pdv == 1:
                pdv = len(DF.loc[idx[index[0],index[1],:,:],:])
                print('starting pdv with row_span: ' + str(pdv))
                column = '<td rowspan="' + str(pdv) + '">' + str(index[1]) + '</td>'
                html_row = html_row + column
            else:
                pdv = pdv - 1

            if total_ub == 1:
                total_ub = len(DF.loc[idx[index[0],index[1],index[2],:],:])
                print('starting ub with row_span: ' + str(total_ub))
                column = '<td rowspan="' + str(total_ub) + '">' + str(index[2]) + '</td>'
                print('should add column: ',column)
                html_row = html_row + column
                column = '<td rowspan="' + str(total_ub) + '">' + str(index[3]) + '</td>'
                html_row = html_row + column
            else:
                total_ub = total_ub - 1

            

        else :
            index_L = len(DF.loc[idx[index[0],index[1],:,:],:])
            # Gran Total Column
            grandTotal = '<td colspan=' + str(2) + '>' + str(index[1])+ '</td>' + '<td colspan=' +str(11) +  '>' + str(index[0]) + '</td>'
            html_row = html_row + grandTotal
            html = html + html_row
            break

        list = row.values.tolist()

        for item in list:
            listColumn = '<td>' + str(item) + '</td>'
            html_row = html_row + listColumn



        html_row = html_row + '</tr>'
        html = html + html_row
        

        
    html = html + '</table>'

    print(html)
    return html

#getActivos2(True,12,2018)







