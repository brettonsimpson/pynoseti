import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import io
import base64

from pynoseti.extract.convert_unix_time import convert_unix_time

def generate_summary(source_index, path, observing_start, observing_end, telescope_list):

    summary_directory = Path(f"{path}/summary")

    if summary_directory.is_dir():
        pass
    
    else:
        summary_directory.mkdir()

    summary = f"""<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>My HTML Page</title>
    </head>
    <body>
        <h1 style="font-size: 40px; margin: 10px 0; padding: 0px 0">PANOSETI Observing Summary</h1>
        
        <h1 style="font-size: 30px; padding: -5px">UTC {observing_start}— UTC {observing_end}</h1>
    </body>
        <u1>
    """

    for source in source_index:

        empty_frame = np.zeros((32,32))
        x=[]
        y=[]

        for position in source.motion_history:
            x.append(position[0][0])
            y.append(position[0][1])

        x = np.array(x)
        y = np.array(y)
        coefficients = np.polyfit(x, y, 1)
        slope, intercept = coefficients
        y_fit = slope * x + intercept
            
        plt.plot(empty_frame)
        plt.plot(x,y_fit, color='red', label='Motion Fit Line')
        plt.scatter(x,y, c='blue', label='Coordinate History')
        plt.gca().invert_yaxis()
        plt.title('Test Source Coordinate History')
        plt.xticks([])
        plt.yticks([])
        plt.legend()
        
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)

        encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")
        buffer.close()
    
        summary += f"""       <p>{source.identifier}</p>
                <p>Time of first detection is {convert_unix_time(int(source.first_detection_time_s))}</p>
                <p>Time of last detection is {convert_unix_time(int(source.last_detection_time_s))}</p>
                <img src="data:image/png;base64,{encoded}">"""
        
        plt.close('all')
        del encoded

    summary += """  </u1>
    </body>
    </html>"""

    with open(f"{path}/summary/summary.html", "w", encoding="utf-8") as file:
        file.write(summary)

    print("HTML file generated successfully!")