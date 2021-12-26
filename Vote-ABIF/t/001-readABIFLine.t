use Test2::V0;
use Test2::Bundle::More;

use Data::Printer;
use ok 'Vote::ABIF';

my $test001 = Vote::ABIF->new( fileIn => 'testfiles/test001.abif' );
$test001->parse();
is_deeply( $test001->metadata, {},
  'file without ABIF header and no metadata has empty meteadata' );

my $test015A = Vote::ABIF->new( fileIn => 'testfiles/test015_headerA.abif' );
$test015A->parse();
is_deeply( $test015A->metadata, {},
  'file with ABIF header and no version or metadata has empty metadata' );

my $test015B = Vote::ABIF->new( fileIn => 'testfiles/test015_headerB.abif' );
$test015B->parse();
is_deeply( $test015B->metadata, { 'version' => '1.0' },
  'file with ABIF header and just the version has only versiopn in  meteadata' );

my $test015C = Vote::ABIF->new( fileIn => 'testfiles/test015_headerC.abif' );
$test015C->parse();
is_deeply( $test015C->metadata, { 'ballot_type' => 'ordinal', 'version' => '1.0' },
  'file with ABIF header and json has meteadata' );


done_testing();
