<?php

/**
 * @file plugins/themes/tvt/TvtThemePlugin.inc.php
 *
 * @class TvtThemePlugin
 * @ingroup plugins_themes_tvt
 *
 * @brief "Talqin va tadqiqotlar" brand theme. A child of the OJS Default theme:
 *  it keeps all Default templates and only adds brand styles and fonts.
 *  Target: OJS 3.3.x
 */

import('lib.pkp.classes.plugins.ThemePlugin');

class TvtThemePlugin extends ThemePlugin {

	/**
	 * Initialize the theme's styles, scripts and hooks. Runs on every request.
	 */
	public function init() {
		// Inherit templates, scripts and styles from the Default theme.
		$this->setParent('defaultthemeplugin');

		$this->addOption('topbarText', 'FieldText', [
			'label' => 'Yuqori panel matni / Текст верхней полосы',
			'description' => 'Shown on the left of the grey utility bar on desktop. Leave empty to hide it.',
			'default' => 'ISSN 2181-3035   Guvohnoma № 1540   Oyiga bir marta',
		]);
		$this->addOption('homepageImageCaption', 'FieldText', [
			'label' => 'Bosh sahifa rasmi izohi / Подпись к изображению главной страницы',
			'description' => 'Caption under the homepage image: what it shows, author and license (required for CC BY-SA photos).',
			'default' => 'Ulugʻbek rasadxonasi, Samarqand. Buyuk sekstantning meridian yoyi, 1420-yillar. Foto: Alaexis, Wikimedia Commons, CC BY-SA 2.5',
		]);

		// Self-hosted brand fonts (Literata, Inter, IBM Plex Mono; SIL OFL).
		$this->addStyle('tvt-fonts', 'styles/fonts.css');

		// Brand styles are compiled together with the Default theme's LESS,
		// so they come after it in the same stylesheet.
		$this->modifyStyle('stylesheet', [
			'addLess' => ['styles/tvt.less'],
			'addLessVariables' =>
				'@tvt-topbar: "' . $this->_cssString($this->getOption('topbarText')) . '";' .
				'@tvt-caption: "' . $this->_cssString($this->getOption('homepageImageCaption')) . '";',
		]);
	}

	/**
	 * Make a theme option safe to embed in a quoted CSS string.
	 *
	 * @param $value string|null
	 * @return string
	 */
	protected function _cssString($value) {
		$value = (string) $value;
		$value = preg_replace('/[\\\\"\'\r\n;{}<>@~`]/u', '', $value);
		return trim(mb_substr($value, 0, 240));
	}

	/**
	 * @copydoc Plugin::getDisplayName()
	 */
	public function getDisplayName() {
		return 'Talqin va tadqiqotlar (TVT)';
	}

	/**
	 * @copydoc Plugin::getDescription()
	 */
	public function getDescription() {
		return 'Brand theme for the "Talqin va tadqiqotlar" journal: navy, gold and ivory palette, Cormorant Garamond and Inter fonts. Child theme of the Default theme.';
	}
}
