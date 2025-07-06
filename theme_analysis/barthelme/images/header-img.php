<?php
$img = 'barthelme-header.jpg';

if ( ! function_exists('imagecreatefromjpeg') )
	die( header("Location: barthelme-header.jpg") );

$default = false;
$vars = array('upper'=>array('r1', 'g1', 'b1'), 'lower'=>array('r2', 'g2', 'b2'));
foreach ( $vars as $var => $subvars ) {
	if ( isset($_GET[$var]) ) {
		foreach ( $subvars as $index => $subvar ) {
			$length = strlen($_GET[$var]) / 3;
			$v = substr($_GET[$var], $index * $length, $length);
			if ( $length == 1 ) $v = '' . $v . $v;
			$$subvar = hexdec( $v );
			if ( $$subvar < 0 || $$subvar > 255 )
			$default = true;
		}
	} else {
		$default = true;
	}
}

if ( $default )
	list ( $r1, $g1, $b1, $r2, $g2, $b2 ) = array ( 138, 154, 174, 186, 200, 218 );

$im = imagecreatefromjpeg($img);
$white = imagecolorat( $im, 15, 15 );
$h = 175;

$corners = array();

for ( $i = 0; $i < $h; $i++ ) {
	$x1 = 0;
	$x2 = 175;
	imageline( $im, $x1, 0 + $i, $x2, 0 + $i, $white );
}

for ( $i = 0; $i < $h; $i++ ) {
	$x1 = 0;
	$x2 = 200;
	$r = ( $r2 - $r1 != 0 ) ? $r1 + ( $r2 - $r1 ) * ( $i / $h ) : $r1;
	$g = ( $g2 - $g1 != 0 ) ? $g1 + ( $g2 - $g1 ) * ( $i / $h ) : $g1;
	$b = ( $b2 - $b1 != 0 ) ? $b1 + ( $b2 - $b1 ) * ( $i / $h ) : $b1;
	$color = imagecolorallocate( $im, $r, $g, $b );
	if ( array_key_exists($i, $corners) ) {
		imageline( $im, $x1, 0 + $i, $x2, 0 + $i, $white );
		list ( $x1, $x2 ) = $corners[$i];
	}
	imageline( $im, $x1, 0 + $i, $x2, 0 + $i, $color );
}

header("Content-Type: image/jpeg");
imagejpeg($im, '', 92);
imagedestroy($im);
?>
