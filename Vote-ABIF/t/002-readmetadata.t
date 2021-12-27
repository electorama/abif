use Test2::V0;
use Test2::Bundle::More;

use Data::Printer;
use ok 'Vote::ABIF';
use Unicode::GCString;
use utf8;
use feature 'unicode_strings';
binmode( STDOUT, ':utf8' );

my $test012 =
  Vote::ABIF->new( fileIn => 'testfiles/test012.abif', DEBUG => 0 );
$test012->parse();
my $expecttest012md = {
  'choices' => {
    'AM'  => "[Adam Muñoz]",
    'DGM' => "[Doña García Márquez]",
    'SBJ' => "[Steven B. Jensen]",
    'SY'  => "[Sue Ye (蘇業)]",
  },
};
is_deeply( $test012->metadata, $expecttest012md,
'file without ABIF header and only choices list generates only generates choices list'
);

my $expect015_meta = {
  'MDATA' => {
    'ballot_type' => "ordinal",
    'choices'     => {},
    'version'     => 1.0
  };
  }
my $test015_meta =
  Vote::ABIF->new( fileIn => 'testfiles/test015_meta.abif', DEBUG => 0 );
$test015_meta->parse();
is_deeply( $test015_meta->metadata, $expect015_meta, '')

p $test015_meta;

# my $test012A = Vote::ABIF->new( fileIn => 'testfiles/test012_headerA.abif' );
# $test012A->parse();
# is_deeply( $test012A->metadata, {},
#   'file with ABIF header and no version or metadata has empty metadata' );

# my $test012B = Vote::ABIF->new( fileIn => 'testfiles/test012_headerB.abif' );
# $test012B->parse();
# is_deeply( $test012B->metadata, { 'version' => '1.0' },
#   'file with ABIF header and just the version has only versiopn in  meteadata' );

# my $test012C = Vote::ABIF->new( fileIn => 'testfiles/test012_headerC.abif' );
# $test012C->parse();
# is_deeply( $test012C->metadata, { 'ballot_type' => 'ordinal', 'version' => '1.0' },
#   'file with ABIF header and json has meteadata' );

done_testing();
