use base Exporter;

use LWP;
use HTTP::Request;
use JSON qw(encode_json);

our @EXPORT = qw(Bot);

package Bot;

sub new {
	my $class = shift;
	my $self = {
		base_url => shift,
		access_token => shift
	};
	bless $self, $class;
	return $self;
}


sub post {
	my $self = shift;
	my $status = shift;
	my $content_warning = shift;
	my $client = LWP::UserAgent->new();
	my $auth_header = "Bearer " . $self->{access_token};
	my %data;
	$data{status} = $status;
	if( $content_warning ) {
		$data{spoiler_text} = $content_warning;
	}
	my $json = JSON::encode_json(\%data);
	my $uri = $self->{base_url} . '/api/v1/statuses';

	my $req = HTTP::Request->new('POST', $uri);
	$req->header('Content-Type' => 'application/json');
	$req->header('Authorization' => $auth_header);
	$req->content($json);
	my $response = $client->request($req);
	if( $response->is_success() ) {
		print("posted");
	} else {
		die("Error: " . $response->status_line() . "\n" );
	}
}

sub get {
	my $self = shift;
	my $client = LWP::UserAgent->new();
	my $response = $client->get("https://mikelynch.org");
	if( $response->is_success() ) {
		print($response->body());
	} else {
		print("Error: " . $response->status_line() . "\n" );
	}
}
