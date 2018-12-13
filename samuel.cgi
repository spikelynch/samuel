#!/usr/bin/perl

# samuel, the last beat poet...

use CGI;

$egotism = .5;      # controls use of 'i' as a subject
$verbosity = .3;    # parameter for number of adjectives and clauses
$haikuness = .3;    # controls line length
$imageness = .5;    # controls choppiness of imagery
$freeness = .3;     # ratio of free to sentencelike stanzas
$length = 5;        # controls number of stanzas
$max_look = 500;    # the maximum number of words we'll get from look 

@NOUN = ( 'computer', 'woman', 'sea', 'happening', 'flower', 'world',
'aardvark', 'tangerine', 'jewel', 'dharma', 'factory', 'supermarket',
'soul', 'heart', 'head', 'feet', 'hand', 'eye', 'fire', 'glass',
'table', 'chair', 'corner', 'bureaucrat', 'consciousness',
'existentiality', 'existence', 'body', 'world', 'buddha-nature',
'karma', 'car', 'tree', 'tower', 'house', 'flugelhorn', 'shout',
'scream', 'howl', 'essence', 'chest', 'road', 'highway', 'poem',
'dust', 'mind', 'brain', 'bones' );

@ADJ = ( 'crazy', 'gone', 'green', 'red', 'blue', 'white', 'yellow',
'purple', 'laughing', 'old', 'ugly', 'young', 'beautiful', 'chrome',
'black', 'smiling', 'cosmic', 'eternal', 'negative', 'evil', 'dirty',
'crying', 'steel', 'crystal', 'singing', 'shouting', 'living', 'lost',
'forgotten', 'dreaming' );

@VERB = ( 'smokes', 'licks', 'takes', 'makes love to', 'loves',
'hates', 'swallows', 'kills', 'drinks', 'eats', 'sees', 'laughs at',
'spurns', 'washes', 'caresses', 'follows', 'talks to', 'speaks to', 'burns', 'finds', 'feels' );

@IVERB = ( 'smoke', 'lick', 'take', 'make love to', 'love', 'hate',
'laugh at', 'kill', 'drink', 'spurn', 'see', 'wash', 'caress',
'follow', 'talk to', 'burn', 'find', 'feel');

@ART = ( 'the', 'my', 'your', 'his', 'her', 'our' ); 

@PRON = ( 'she', 'it', 'he' );

@IPRON = ( 'they', 'you', 'i', 'i', 'i', 'i', 'i', 'we' );

@CONJ = ( 'while', 'as', 'and', 'but', 'so', 'if', 'when', 'until', 'or' );

sub spc {
    my ( $space );
    $lwords++;
    if( rand() < $lwords * $haikuness * .5 ) {
	$lwords = 0;
	$space = '<br>';
    } else {
	$space = ' ';
    }
    $space;
}

sub atom {
    my ( $which ) = int(rand($#_ + 1));
    if( rand() < $imageness ) {
	$image_word = $_[$which];
    }
    $_[$which];
}


sub linked_noun {
    my( $ln, $new );
    while( 1 ) {
	if( !defined @used_nouns || rand() < $imageness ) {
	    $ln = &atom(@NOUN);
	    $new = 1;
	} else {
	    $ln = &atom(@used_nouns);
	}
	last if( ! defined($done_nouns{$ln}) );
    }
    push @used_nouns, $ln if( $new == 1 );
    $done_nouns{$ln} = 'done';
    $ln;
}

sub complex_noun {
    my ( $cn );
    if( rand() < $verbosity ) {
	$cn = &atom(@ADJ) . &spc;
    }
    $cn .= &linked_noun;
    $cn;
}
    

sub fancy_noun {
    my ( $r ) = rand();
    my ( $fn );
    if( $r < .6 ) {
	&atom(@ART) . &spc . &complex_noun;
    } elsif( $r < .8 ) {
	&atom(@ART) . &spc . &complex_noun . "'s" . &spc . &complex_noun;
    } else {
	'the' . &spc . &complex_noun . &spc . 'of' . &spc . &atom(@ART) . &spc . &complex_noun;
    }
}


sub subject_and_verb {
    if( rand() < $egotism ) {
	&atom(@IPRON) . &spc . &atom(@IVERB);
    } elsif( rand() < $egotism ) {
	&atom(@PRON) . &spc . &atom(@VERB); 
    } else {
        &fancy_noun . &spc . &atom(@VERB);
    }
}


sub sentence {
    undef %done_nouns;
    &subject_and_verb . &spc. &fancy_noun;
}


	

sub sentence_stanza {
    my ( $fs ) = &sentence;
    if( rand() < $verbosity ) {
	$fs .= &spc . &atom(@CONJ) . &spc . &sentence;
    } 
    if( rand() < $verbosity ) {
	$fs .= &spc . &atom(@CONJ) . &spc . &sentence;
    } 
    $fs;
}


sub look_up_nouns {
    my ( $key ) = shift;
    my ( $count ) = 0;
    $key = substr($key, 0, 3);
    open(LOOKUP, "look '$key' |");
    undef @image_nouns;
    while( <LOOKUP> ) {
	chomp;
	push @image_nouns, lc($_);
	$count++;
	last if ( $count > $max_look );
    }
    close(LOOKUP);
}


sub free_form_stanza {
    my( $fs, $n, $nwords, $length);
    if( !defined $image_word ) {
	$image_word = &atom(@NOUN);
	$fs = $image_word;
    } else {
	&look_up_nouns($image_word);
	$fs = $image_word;
	$length = int(rand($haikuness * 5) + rand($haikuness * 5) + 3);
	while( $nwords < $length ) {
	    $n = &atom(@image_nouns);
	    push @used_nouns, $n;
	    $fs .= &spc . $n;
	    $nwords++;
	}
    }
    $fs;
}



sub stanza {
    if( rand() < $freeness ) {
	&free_form_stanza;
    } else {
	&sentence_stanza;
    }
}



sub start_page {

    print<<EOHTML;
Content-type: text/html

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2//EN">
<html>
<head>

<title>Samuel</title>
</head>

<body bgcolor="#edcb95" text="#000000" link="#d30000" vlink="#800000">

<table width="100%"><tr><td align="center">
<table width="50%"><tr><td align="left">
<p><a href="./"><img alt="Picture of Samuel" src="./Samuel.gif" border=0></a></p>
<p>&nbsp;</p>
<strong>
EOHTML

}

sub end_page {
    print<<EOHTML;
</strong>

    <p>&nbsp;</p>

<p><form method="GET" action="./">
<input type="submit" value="another poem, man">
</form></p>

<p><strong><a href="about.html">samuel, beat poet</a></strong></p>
<p><strong><a href="technical.html">more about samuel</a></strong></p>
<p><strong><a href="https://mikelynch.org/">back to mike's</a></strong></p>

</td></tr></table>

<table>
<tr><td align="left">
<img alt="--" src="./shortbar.gif" border=0><br>
</td></tr></table>

</td></tr></table>

</body>
</html>
EOHTML
}



######### main ###########

$nstanza = 2 + int(rand($length / 2)) + int(rand($length / 2));

&start_page;

$fake = srand(time ^ $$);

for( 1..$nstanza ) {
    print "<p>" . &stanza . "</p>\n";
}


&end_page;
