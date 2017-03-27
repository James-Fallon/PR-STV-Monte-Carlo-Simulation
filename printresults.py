import plotly.plotly as pltly
import plotly.graph_objs as go
import webbrowser



def main (candidateData, chancesOfWinning, mostCommonOutcome):

    #Create bar chart to display each candidate's chance of winning a seat

    candidates = [row[2] + ' ' + row[1] for row in candidateData]

    layout = go.Layout(
        autosize=False,
        width=500,
        height=500,
        margin=go.Margin(
            l=150,
            r=50,
            b=100,
            t=50,
            pad=2
        )
    )

    data = [go.Bar(
                x=chancesOfWinning,
                y=candidates,
                orientation = 'h'
    )]

    fig = go.Figure(data=data, layout=layout)

    plotUrl = pltly.plot(fig, filename='horizontal-bar', auto_open=False,)

    #Store the html used to display this chart

    chanceOfWinningChartHtml = '''<h2>Chance of winning a seat: </h2>
                                    <iframe width="1000" height="500" frameborder="0" seamless="seamless" scrolling="no" \
                                    src="''' + plotUrl + '''.embed?width=800&height=550"></iframe>
                                    '''

    #Create a html table with the most common outcome

    mostCommonOutcomeTableHtml = '''<h2>Most common outcome:</h2>
    <table>
      <tr>
        <th>Candidate</th>
        <th>Party</th>
      </tr>
    '''

    for element in mostCommonOutcome:
        mostCommonOutcomeTableHtml = mostCommonOutcomeTableHtml + '''<tr>
          <td>''' + candidates[int(element)] +'''</td>
          <td><img src="assets/party-logos/''' + candidateData[int(element)][3] + '''.png" alt="" style="width:125px; height:50px;"></td>
        </tr>
        '''

    mostCommonOutcomeTableHtml = mostCommonOutcomeTableHtml + '</table>'

    #Now we add these results to a basic html format and print this to a file

    f = open('results.html','w')

    html_string = '''
    <html>
        <head>
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
            <style>
                body{
                    margin:0 100; background:whitesmoke;
                }
                table {
                    font-family: arial, sans-serif;
                    border-collapse: collapse;
                    width: 100%;
                }
                td, th {
                    border: 1px solid #dddddd;
                    text-align: left;
                    padding: 8px;
                }
                tr:nth-child(even) {
                    background-color: #dddddd;
                }
            </style>
        </head>
        <body>
            <h1>Galway-West Local Election</h1>

            ''' + mostCommonOutcomeTableHtml + chanceOfWinningChartHtml + '''
        </body>
    </html>'''


    f.write(html_string)
    f.close()

    #Change path to reflect file location
    filename = 'file:///Users/jamesfallon/IdeaProjects/PR-STV-Software-Model/' + 'results.html'
    webbrowser.open_new_tab(filename)
