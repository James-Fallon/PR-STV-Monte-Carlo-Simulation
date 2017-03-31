import plotly.plotly as pltly
import plotly.graph_objs as go
import webbrowser
import operator



def main (candidateData, chancesOfWinning, outcomes, numberOfSeats):

    #Create bar chart to display each candidate's chance of winning a seat

    candidates = [row[2] + ' ' + row[1] for row in candidateData]
    candidateFirstName = [row[2] for row in candidateData]
    candidateSurname = [row[1] for row in candidateData]

    sorted_numberOfWinsPerCandidate = sorted(zip(candidates,chancesOfWinning), key=operator.itemgetter(1))

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

    sortedChanceOfWinning = map(list, zip(*sorted_numberOfWinsPerCandidate))

    data = [go.Bar(
                x=sortedChanceOfWinning[1],
                y=sortedChanceOfWinning[0],
                orientation = 'h',
                marker=dict(color = '#1ABC9C')
    )]

    fig = go.Figure(data=data, layout=layout)

    plotUrl = pltly.plot(fig, filename='horizontal-bar', auto_open=False,)

    #Store the html used to display this chart

    chanceOfWinningChartHtml = '''<h2>Chance of Winning a Seat: </h2>
                                    <iframe width="1000" height="500" frameborder="0" seamless="seamless" scrolling="no" \
                                    src="''' + plotUrl + '''.embed?width=800&height=550"></iframe>
                                    '''

    #Create a html table with the most common outcome

    mostCommonOutcomeTableHtml = '''
    <h2>Most Common Outcomes: </h2>
    <div class="scrollingTable">
    <table id="myTable">
      <tr>
        <th>Number of<br>Occurences</th>
        <th colspan="'''+str(numberOfSeats)+'''">Outcome</th>
      </tr>
    '''

    for i in range(len(outcomes)):
        outcome,frequency = outcomes[i]
        outcome = list(outcome)
        mostCommonOutcomeTableHtml = mostCommonOutcomeTableHtml + '<tr><td align="center" width="1%">' + str(frequency) + '</td>'
        for element in outcome:
            mostCommonOutcomeTableHtml = mostCommonOutcomeTableHtml + '''
              <td align="left"><img src="assets/party-logos/''' + candidateData[int(element)][3] + '''.png" alt="" style="width:50px; height:25px;">&emsp;''' + candidateFirstName[int(element)] + '''&nbsp;''' + candidateSurname[int(element)] + '''</td>
            '''
        mostCommonOutcomeTableHtml = mostCommonOutcomeTableHtml + '</tr>'
    mostCommonOutcomeTableHtml = mostCommonOutcomeTableHtml + '</table></div>'

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
                    border:2px solid #1ABC9C;
                    width: 100%;
                }
                td + td{
                    font-size: 10px;
                    border: 1px solid #dddddd;
                    padding: 8px;
                }
                td{
                    font-size: 16px;
                    border-left: 2px solid #1ABC9C;
                    border-right: 2px solid #1ABC9C;
                    padding: 8px;
                }
                th {
                    border: 1px solid #1ABC9C;
                    background:#1ABC9C;
                    text-align: center;
                    color:white;
                    font-size: 16px;
                    padding: 8px;
                }
                tr:nth-child(even) {
                    background-color: #dddddd;
                }
                .scrollingTable {
                    width: 100%;
                    overflow-y: auto;
                }
            </style>
            <script type="text/javascript">
            function makeTableScroll() {
                // Constant retrieved from server-side via JSP
                var maxRows = 6;

                var table = document.getElementById('myTable');
                var wrapper = table.parentNode;
                var rowsInTable = table.rows.length;
                var height = 0;
                if (rowsInTable > maxRows) {
                    for (var i = 0; i < maxRows; i++) {
                        height += table.rows[i].clientHeight;
                    }
                    wrapper.style.height = height + "px";
                }
        }
    </script>
        </head>
        <body onload="makeTableScroll();">
            <h1>Monte Carlo Simulation Results: Galway-West</h1>

            ''' + mostCommonOutcomeTableHtml + chanceOfWinningChartHtml + '''
        </body>
    </html>'''


    f.write(html_string)
    f.close()

    #Change path to reflect file location
    filename = 'file:///Users/jamesfallon/IdeaProjects/PR-STV-Software-Model/' + 'results.html'
    webbrowser.open_new_tab(filename)
