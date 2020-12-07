import os
import json
import logging
from flask import Flask, render_template, jsonify, request



app = Flask(__name__)
num_leds = 250
current_lighting_state = {x: (0,0,0) for x in range(0, num_leds)}
current_feature = []


# logging
gunicorn_error_logger = logging.getLogger('gunicorn.error')
app.logger.handlers.extend(gunicorn_error_logger.handlers)
app.logger.setLevel(logging.DEBUG)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False


def convert_hex_to_rgb(hex_colour):
    """Converts hex string to rgb"""
    h = hex_colour.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


@app.route('/')
def index():
    """API index route"""
    return render_template('index.html')


@app.route('/state/')
def get_current_state():
    """Get state"""
    if current_feature:
        return jsonify({
            'feature': current_feature.pop(0),
        })
    return jsonify(current_lighting_state)


def convert_x_value_to_rgb_string_index(x):
    """Converts the graph's x value to the LED index"""
    maximum_x = 100
    minimum_x = 0
    if x > maximum_x:
        x = maximum_x
    if x < minimum_x:
        x = minimum_x
    return round((x / maximum_x) * (num_leds - 1))


def convert_percent_to_string_index(percent_value):
    maximum = 100
    minimum = 0
    if percent_value > maximum:
        percent_value = maximum
    if percent_value < minimum:
        percent_value = minimum
    range_lower = int((percent_value+0)/float(100) * num_leds)
    range_upper = int((percent_value+1)/float(100) * num_leds)
    if range_upper >= num_leds:
        range_upper = num_leds - 1
    return range(range_lower, range_upper)


@app.route('/update/', methods=['POST'])
def update_state():
    """API index route"""
    diff = json.loads(request.form.get('diff'))
    print(request.form)
    if not diff:
        return jsonify({'status': 'error'})
    i = 0
    for hex_colour in diff:
        leds = convert_percent_to_string_index(i)
        for led in leds:
            if hex_colour:
                rgb = convert_hex_to_rgb(hex_colour)
                current_lighting_state[led] = rgb
        i += 1
    return jsonify({'status': 'ok'})


@app.route('/feature/', methods=['GET'])
def custom_feature():
    """Handle custom features"""
    requested_feature = request.args.get('feature')
    if requested_feature == 'flash':
        current_feature.append('flash')
    elif requested_feature == 'pinwheel':
        current_feature.append('pinwheel')
    elif requested_feature == 'chase':
        current_feature.append('chase')
    elif requested_feature == 'twinkle':
        current_feature.append('twinkle')
    return jsonify({'status': 'ok'})


@app.route('/clear/', methods=['GET'])
def clear_lights():
    """Handle custom features"""
    for i in range(0, num_leds - 1):
        current_lighting_state[i] = [0, 0, 0]
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', '8000')))
