<?php
/**
 * Plugin Name: Lead Generation Calculator
 * Description: Estimates monthly lead value with validated numeric inputs.
 * Version: 1.0.0
 * Author: Md Adib Azam
 * License: GPL-2.0-or-later
 */

if (!defined('ABSPATH')) {
    exit;
}

function adib_22_lead_generation_calculator_render($attributes = []) {
    $values = [];
    $notice = '';
    if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['adib_22_lead_generation_calculator_nonce']) && wp_verify_nonce(sanitize_text_field(wp_unslash($_POST['adib_22_lead_generation_calculator_nonce'])), 'adib_22_lead_generation_calculator_submit')) {
        $values['monthly_visitors'] = isset($_POST['adib_22_lead_generation_calculator_monthly_visitors']) ? absint(wp_unslash($_POST['adib_22_lead_generation_calculator_monthly_visitors'])) : '';
        $values['conversion_rate'] = isset($_POST['adib_22_lead_generation_calculator_conversion_rate']) ? floatval(wp_unslash($_POST['adib_22_lead_generation_calculator_conversion_rate'])) : '';
        $values['lead_value'] = isset($_POST['adib_22_lead_generation_calculator_lead_value']) ? floatval(wp_unslash($_POST['adib_22_lead_generation_calculator_lead_value'])) : '';
        $visitors = (float) $values['monthly_visitors'];
        $rate = (float) $values['conversion_rate'];
        $lead_value = (float) $values['lead_value'];
        $estimate = $visitors * ($rate / 100) * $lead_value;
        $notice = '<p role="status">Estimated monthly lead value: ₹' . esc_html(number_format_i18n($estimate, 2)) . '</p>';
    }
    $html = '<section class="adib_22_lead_generation_calculator-component"><h2>Lead Generation Calculator</h2>' . $notice . '<form method="post">';
    $html .= wp_nonce_field('adib_22_lead_generation_calculator_submit', 'adib_22_lead_generation_calculator_nonce', true, false);
    $html .= '<label>Monthly Visitors<input name="adib_22_lead_generation_calculator_monthly_visitors" type="number" required></label>';
    $html .= '<label>Conversion Rate<input name="adib_22_lead_generation_calculator_conversion_rate" type="number" required></label>';
    $html .= '<label>Lead Value<input name="adib_22_lead_generation_calculator_lead_value" type="number" required></label>';
    $html .= '<button type="submit">Submit</button></form></section>';
    return $html;
}
add_shortcode('adib_22_lead-generation-calculator', 'adib_22_lead_generation_calculator_render');

function adib_22_lead_generation_calculator_assets() {
    $css = '.adib_22_lead_generation_calculator-component{max-width:760px;padding:1.5rem;border:1px solid #dbe4f0;border-radius:1rem}'
         . '.adib_22_lead_generation_calculator-component label{display:block;margin:.8rem 0}'
         . '.adib_22_lead_generation_calculator-component input{display:block;width:100%;max-width:34rem;padding:.65rem}'
         . '.adib_22_lead_generation_calculator-component button{padding:.7rem 1.1rem;cursor:pointer}'
         . '.adib_22_lead_generation_calculator-component dt{font-weight:700;margin-top:.75rem}';
    wp_register_style('adib_22_lead_generation_calculator', false, [], '1.0.0');
    wp_enqueue_style('adib_22_lead_generation_calculator');
    wp_add_inline_style('adib_22_lead_generation_calculator', $css);
}
add_action('wp_enqueue_scripts', 'adib_22_lead_generation_calculator_assets');
