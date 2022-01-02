package Vote::ABIF;
use 5.026;
use feature qw/signatures postderef/;
no warnings 'experimental';
# use utf8::all;
# use feature 'unicode_strings';
# binmode(STDOUT,':utf8');

use Path::Tiny;
# syntax compatible with new experimental try/catch feature that can be used with older perls.
# on 5.34+ it just enables the builtin 'try' feature.
use Feature::Compat::Try;
use Cpanel::JSON::XS;

use Data::Printer;

=pod

=head1 NAME

Vote::ABIF

=head1 DESCRIPTION

=head1 SYNOPSIS

=head1 ARGUMENTS

=cut

=head2 fileIn

Name of file to read. Required.

=head2 ballotType

Sets the type of ballot to use if a valid type is not specified in metadata.

=head2 ballotTypeForce

Ignore ballot type if present in the metadata and use the provided ballot type.

=cut

sub new ( $class, %args ) {
  my $self = {};
  $self->{'MDATA'}            = {};
  $self->{'currentlist'}      = 'choices';
  $self->{'MDATA'}{'choices'} = {};
  $self->{'finishedmetadata'} = 0;
  $self->{'DEBUG'}            = 0;
  while ( my ( $key, $value ) = each %args ) {
    $self->{$key} = $value;
  }
  return bless $self, $class;
}

my $JSON = Cpanel::JSON::XS->new;

sub metadata ( $I, $key = 0, $value = '' ) {
  warn "metadata called: key $key value $value" if $I->{'DEBUG'};
  if ($key) {
    if ($value) { $I->{'MDATA'}->{$key} = $value }
    else        { return $I->{'MDATA'}->{$key} }
  }
  else {
    return $I->{'MDATA'};
  }
}

sub ballotType ($I) { return $I->{'ballotType'} }

sub _parseABIFHead ( $I, $line ) {
  no warnings 'uninitialized';
  $line =~ /(?<abifver>\d+\.\d+)(?<json>.*)/;
  $I->metadata( 'version', $+{abifver} ) if $+{abifver};
  if ( $+{json} ) {
    my $exdata = $JSON->decode( $+{json} );
    for my $k ( keys %{$exdata} ) { $I->metadata( $k, $exdata->{$k} ) }
  }
}

sub _parseMetaData ( $I, $line ) {

  warn "parsing: $line";
  if ( $line =~ /^\@(\w+)/ ) {    # list name directive
    $I->{'currentlist'} = $1;
  }
  elsif ( $line =~ /^=/ ) {       # list item
        # utf8::decode( $line); # perl regexes use legacy encoding
    my ( $key, $value ) = $line =~ /^=\s*(\w+)\s*:\s*(.*)/;
    $value =~ s/\s+$//g;
    # utf8::encode( $value ); # back to utf8.
    $I->{'MDATA'}{ $I->{'currentlist'} }{$key} = $value;
  }
  else {
    my ( $key, $value ) = $line =~ /^\s*(\w+)\s*:\s*(.*)/;
    $value =~ s/\s+$//g;
    $I->metadata( $1, $2 );
  }
}

sub _validateMetaData ($I) {
  $I->{'finishedmetadata'} = 1;
  # ...
}

sub _ordinalline( $I, $line ) {
  my $res = {};
  my $rank = -1;
  my ( $count, $ballot ) = $line =~ /(.*):(.*)/; #split ( ':', $line) ;
  $res->{'count'} = int $count;
  for my $set ( split ( '>', $ballot) ) {
    for my $equals ( split ( '=', $set) ) {
      $equals =~ s/^\s+|\s+$//g;
      $equals =~ s/\[|\]//g;
      $res->{ $equals } = $rank;
    }
    $rank--;
  }
  return $res;
}

sub _parseballots ($I, $line) {
  $I->_ordinalline( $line ) if $I->ballotType eq 'ordinal';
}

sub parse ($I) {
  my $linectr = 1;
  my @input   = path( $I->{'fileIn'} )->lines_utf8( { chomp => 1 } );
  if ( $input[0] =~ /^ABIF/ ) {
    $I->_parseABIFHead( shift @input );
    $linectr++;
  }
INPUTPARSELOOP1: while (@input) {
    my $line = shift @input;
    next INPUTPARSELOOP1 if $line =~ /^#/;    # line is a comment
    next INPUTPARSELOOP1 if $line !~ /\w/;    # line is empty
    if ( $line =~ /^\d/ ) {
      if ( !$I->{'finishedmetadata'} ) { $I->_validateMetaData() }
      # ... parse the ballot data line
    }
    else {
      $I->_parseMetaData($line);
    }

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
