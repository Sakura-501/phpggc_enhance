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
}
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
}
namespace PHPUnit\Framework\MockObject\Stub{
    class ReturnCallback
    {
        private $callback;
        public function __construct($callback)
        {
            $this->callback = $callback;
        }
    }
}
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
}

