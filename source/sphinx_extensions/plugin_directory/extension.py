import os
import os.path
import shutil

import jinja2
import qiime.sdk


def generate_rst(app):
    plugins = qiime.sdk.PluginManager().plugins
    loader = jinja2.PackageLoader('sphinx_extensions.plugin_directory',
                                  'templates')
    env = jinja2.Environment(loader=loader)

    rst_dir = os.path.join(app.env.srcdir, 'plugins', 'available')
    app.plugin_directory_rst_dir = rst_dir
    cleanup_rst(app, None)
    os.mkdir(rst_dir)

    index_path = os.path.join(rst_dir, 'index.rst')
    with open(index_path, 'w') as fh:
        template = env.get_template('available.rst')
        rendered = template.render(plugins=plugins)
        fh.write(rendered)

    for plugin in plugins.values():
        plugin_dir = os.path.join(rst_dir, plugin.name)
        os.mkdir(plugin_dir)

        index_path = os.path.join(plugin_dir, 'index.rst')
        with open(index_path, 'w') as fh:
            template = env.get_template('plugin.rst')
            rendered = template.render(plugin=plugin)
            fh.write(rendered)

        for action in plugin.actions.values():
            action_path = os.path.join(plugin_dir, '%s.rst' % action.id)
            with open(action_path, 'w') as fh:
                title = '%s: %s' % (action.id, action.name)

                input_specs = _get_param_specs(action.signature, 'inputs')
                parameter_specs = _get_param_specs(action.signature,
                                                   'parameters')
                output_specs = _get_param_specs(action.signature, 'outputs',
                                                no_default='N/A')

                template = env.get_template('action.rst')
                rendered = template.render(action=action, title=title,
                                           input_specs=input_specs,
                                           parameter_specs=parameter_specs,
                                           output_specs=output_specs)
                fh.write(rendered)


def _get_param_specs(signature, group, no_default='Required'):
    specs = []
    for name, (qiime_type, _) in getattr(signature, group).items():
        default = no_default
        if name in signature.defaults:
            default = signature.defaults[name]
        specs.append((name, qiime_type, default))
    return specs


def cleanup_rst(app, exception):
    if hasattr(app, 'plugin_directory_rst_dir') and \
            os.path.exists(app.plugin_directory_rst_dir):
        shutil.rmtree(app.plugin_directory_rst_dir)


def setup(app):
    app.connect('builder-inited', generate_rst)
    app.connect('build-finished', cleanup_rst)
    return {'version': '0.0.1'}
