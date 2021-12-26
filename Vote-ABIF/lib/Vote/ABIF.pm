
package Vote::ABIF;
use Moo;
use 5.026;
use feature qw/signatures postderef/;
no warnings 'experimental';

use namespace::clean;
use Path::Tiny;
# syntax compatible with new experimental try/catch feature that can be used with older perls.
# on 5.34+ it just enables the builtin 'try' feature.
use Feature::Compat::Try;
use Cpanel::JSON::XS;

=pod

=head1 NAME

Vote::ABIF

=head1 DESCRIPTION

=head1 SYNOPSIS

=head1 ARGUMENTS

=cut

=head2 fileIn

Name of file to read. Required.

=cut

has fileIn => (
  is       => 'ro',
  required => 1,
);

=head2 ballotType

Sets the type of ballot to use if a valid type is not specified in metadata.

=cut

has ballotType => (
  is      => 'rw',
  default => 0,
);

=head2 ballotTypeForce

Ignore ballot type if present in the metadata and use the provided ballot type.

=cut

has ballotTypeForce => (
  is      => 'ro',
  default => 0,
);

has _METADATA => (
  is      => 'rw',
  default =>  {} ,
);

has _currentlist => (
  is      => 'rw',
  default => 'choices',
);

has _finished_metadata => (
  is      => 'rw',
  default => 0,
);

has _log => (
  is  => 'rw',
  isa => sub { [] },
);

sub log ( $I, $level, $message ) {
  my $l = $I->_log();
  push $l->@*, ( { $level, $message } );
}

my $JSON = Cpanel::JSON::XS->new;

sub metadata ( $I, $key = 0, $value = '' ) {
  if ($key) {
    if ($value) { $I->{'_METADATA'}->{$key} = $value }
    else        { return $I->{'_METADATA'}->{$key} }
  }
  else {
    return $I->{'_METADATA'};
  }
}

sub parseABIFHead ( $I, $line ) {
  no warnings 'uninitialized';
  $line =~ /(?<abifver>\d+\.\d+)(?<json>.*)/;
  $I->metadata( 'version', $+{abifver} ) if $+{abifver};
  if ( $+{json} ) {
    my $exdata = $JSON->decode( $+{json} );
    for my $k ( keys %{$exdata} ) { $I->metadata( $k, $exdata->{$k} ) }
  }
}

sub _parseMetaData ( $I, $line ) {
  if ( $line =~ /^\@(\w+)/ ) {    # list name directive
    $I->_currentlist($1);
  }
  elsif ( $line =~ /^=/ ) {       # list item
    $line =~ /^=\s*(\w+)\s*:\s*(.*)\s$/;
    $I->metadata( $1, $2 );
  }
  else {
    $line =~ /^\s*(\w+)\s*:\s*(.*)\s$/;
    $I->metadata( $1, $2 );
   }
}

sub _validateMetaData ($I) {
  $I->_finished_metadata(1);
  # ...
}

sub parse ($I) {
  my $linectr = 1;
  my @input   = path( $I->fileIn )->lines_utf8( { chomp => 1 } );
  if ( $input[0] =~ /^ABIF/ ) {
    $I->parseABIFHead( shift @input );
    $linectr++;
  }
INPUTPARSELOOP1: for my $line (@input) {
    next INPUTPARSELOOP1 if $line =~ /^#/;    # line is a comment
    next INPUTPARSELOOP1 if $line !~ /\w/;    # line is empty
    if ( $line =~ /^\d/ ) {
      if ( !$I->_finished_metadata ) { $I->_validateMetaData() }
      # ... parse the ballot data line
    }
    $I->_parseMetaData($line);

    $linectr++;
  }
  # INPUTPARSELOOP2: for my $line (@input) {
  #     next INPUTPARSELOOP2 if $line =~ /^#/;

#     # if( $line !~ /^\d/) {
#     #   warn "Ignoring MetaData after Ballot Data Line: $linectr: $line\n" ;
#     # }

  #     $linectr++
  #   }
}

=pod

=head1 AUTHORS

=head1 COPYRIGHT

=cut

1;
