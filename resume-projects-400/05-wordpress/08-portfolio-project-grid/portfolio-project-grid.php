<?php
/**
 * Plugin Name: Portfolio Project Grid
 * Description: Creates a filter-friendly portfolio project grid.
 * Version: 1.0.0
 * Author: Md Adib Azam
 * License: GPL-2.0-or-later
 */

if (!defined('ABSPATH')) {
    exit;
}

function adib_08_portfolio_project_grid_render($attributes = []) {
    $attributes = shortcode_atts([
        'project' => '',
        'technology' => '',
        'url' => ''
    ], $attributes, 'adib_08_portfolio-project-grid');
    $html = '<section class="adib_08_portfolio_project_grid-component"><h2>Portfolio Project Grid</h2><dl>';
    if ($attributes['project'] !== '') { $html .= '<dt>Project</dt><dd>' . esc_html($attributes['project']) . '</dd>'; }
    if ($attributes['technology'] !== '') { $html .= '<dt>Technology</dt><dd>' . esc_html($attributes['technology']) . '</dd>'; }
    if ($attributes['url'] !== '') { $html .= '<dt>Url</dt><dd>' . esc_html($attributes['url']) . '</dd>'; }
    $html .= '</dl></section>';
    return $html;
}
add_shortcode('adib_08_portfolio-project-grid', 'adib_08_portfolio_project_grid_render');

function adib_08_portfolio_project_grid_assets() {
    $css = '.adib_08_portfolio_project_grid-component{max-width:760px;padding:1.5rem;border:1px solid #dbe4f0;border-radius:1rem}'
         . '.adib_08_portfolio_project_grid-component label{display:block;margin:.8rem 0}'
         . '.adib_08_portfolio_project_grid-component input{display:block;width:100%;max-width:34rem;padding:.65rem}'
         . '.adib_08_portfolio_project_grid-component button{padding:.7rem 1.1rem;cursor:pointer}'
         . '.adib_08_portfolio_project_grid-component dt{font-weight:700;margin-top:.75rem}';
    wp_register_style('adib_08_portfolio_project_grid', false, [], '1.0.0');
    wp_enqueue_style('adib_08_portfolio_project_grid');
    wp_add_inline_style('adib_08_portfolio_project_grid', $css);
}
add_action('wp_enqueue_scripts', 'adib_08_portfolio_project_grid_assets');
