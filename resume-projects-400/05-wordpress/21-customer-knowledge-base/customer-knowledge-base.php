<?php
/**
 * Plugin Name: Customer Knowledge Base
 * Description: Collects a knowledge-base question and suggests a search.
 * Version: 1.0.0
 * Author: Md Adib Azam
 * License: GPL-2.0-or-later
 */

if (!defined('ABSPATH')) {
    exit;
}

function adib_21_customer_knowledge_base_render($attributes = []) {
    $values = [];
    $notice = '';
    if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['adib_21_customer_knowledge_base_nonce']) && wp_verify_nonce(sanitize_text_field(wp_unslash($_POST['adib_21_customer_knowledge_base_nonce'])), 'adib_21_customer_knowledge_base_submit')) {
        $values['question'] = isset($_POST['adib_21_customer_knowledge_base_question']) ? sanitize_text_field(wp_unslash($_POST['adib_21_customer_knowledge_base_question'])) : '';
        $values['email'] = isset($_POST['adib_21_customer_knowledge_base_email']) ? sanitize_email(wp_unslash($_POST['adib_21_customer_knowledge_base_email'])) : '';
        $values['topic'] = isset($_POST['adib_21_customer_knowledge_base_topic']) ? sanitize_text_field(wp_unslash($_POST['adib_21_customer_knowledge_base_topic'])) : '';
        $notice = '<p role="status">Request validated for review. No personal data was stored by this demo plugin.</p>';
    }
    $html = '<section class="adib_21_customer_knowledge_base-component"><h2>Customer Knowledge Base</h2>' . $notice . '<form method="post">';
    $html .= wp_nonce_field('adib_21_customer_knowledge_base_submit', 'adib_21_customer_knowledge_base_nonce', true, false);
    $html .= '<label>Question<input name="adib_21_customer_knowledge_base_question" type="text" required></label>';
    $html .= '<label>Email<input name="adib_21_customer_knowledge_base_email" type="email" required></label>';
    $html .= '<label>Topic<input name="adib_21_customer_knowledge_base_topic" type="text" required></label>';
    $html .= '<button type="submit">Submit</button></form></section>';
    return $html;
}
add_shortcode('adib_21_customer-knowledge-base', 'adib_21_customer_knowledge_base_render');

function adib_21_customer_knowledge_base_assets() {
    $css = '.adib_21_customer_knowledge_base-component{max-width:760px;padding:1.5rem;border:1px solid #dbe4f0;border-radius:1rem}'
         . '.adib_21_customer_knowledge_base-component label{display:block;margin:.8rem 0}'
         . '.adib_21_customer_knowledge_base-component input{display:block;width:100%;max-width:34rem;padding:.65rem}'
         . '.adib_21_customer_knowledge_base-component button{padding:.7rem 1.1rem;cursor:pointer}'
         . '.adib_21_customer_knowledge_base-component dt{font-weight:700;margin-top:.75rem}';
    wp_register_style('adib_21_customer_knowledge_base', false, [], '1.0.0');
    wp_enqueue_style('adib_21_customer_knowledge_base');
    wp_add_inline_style('adib_21_customer_knowledge_base', $css);
}
add_action('wp_enqueue_scripts', 'adib_21_customer_knowledge_base_assets');
