#include <stdio.h>
#include <utility>
#include <memory>
#include <cstring>

using namespace std;

template<class T>
class Object
{
	public:
	Object(T data)
	{
		ptr = unique_ptr<T>(data);
	}

	~Object()
	{
	}
	protected:
	unique_ptr<T> ptr;
};

template<>
class Object<void *>
{
	struct PtrContext
	{
		void *ptr;
		int ref_cnt;
		int size;
	};
	void AllocateContext(int size = 0)
	{
		context = new PtrContext;
		context->ref_cnt = 0;
		if (size > 0) {
			context->ptr = new char[size];
			context->ref_cnt++;
		} else {
			context->ptr = NULL;
		}
		context->size = size;
		printf("Object %p, allocated context %p size %d ref_cnt %d\n", this, context, size, context->ref_cnt);
	}
	void DisposeContext(void)
	{
		if (!context)
			return;

		printf("Object %p, disposing context %p ref_cnt %d\n", this, context, context->ref_cnt);

		if (context->ref_cnt > 0)
			context->ref_cnt--;

		if (!context->ref_cnt) {
			if (context->ptr) {
				delete [] (char *)context->ptr;
				context->ptr = NULL;
				context->size = 0;
			}
			delete context;
			context = NULL;
		}
	}
	public:
	Object(int size)
	{
		AllocateContext(size);
	}
	Object()
	{
		AllocateContext();
	}
	Object(Object &&obj)
	{
		context = obj.context;
		obj.context = NULL;
		printf("Move ctor called moved context %p from %p to %p ref_cnt %d\n", context, &obj, this, context->ref_cnt);
	}
	Object(Object &obj)
	{
		context = obj.context;
		context->ref_cnt++;
		printf("Copy ctor called copied context %p from %p to %p ref_cnt %d\n", context, &obj, this, context->ref_cnt);
	}
	Object &operator=(Object &&obj)
	{
		if (context != obj.context) {
			DisposeContext();
			context = obj.context;
			obj.context = NULL;
		} else {
			printf("Loop detected, objects %p and %p have already same context %p\n",
				this, &obj, context);
		}
		printf("Move operator= called moved context %p from %p to %p ref_cnt %d\n", context, &obj, this, context->ref_cnt);
		return *this;
	}
	Object &operator=(Object &obj)
	{
		if (context != obj.context) {
			DisposeContext();
			context = obj.context;
			context->ref_cnt++;
		} else {
			printf("Loop detected, objects %p and %p have already same context %p\n",
				this, &obj, context);
		}
		printf("Copy operator= called copied context %p from %p to %p ref_cnt %d\n", context, &obj, this, context->ref_cnt);
		return *this;
	}

	void *operator*(void)
	{
		if (!context)
			return NULL;
		if (context->ref_cnt > 1) {
			PtrContext *tmp_context = new PtrContext;
			tmp_context->ptr = new char[context->size];
			tmp_context->size = context->size;
			tmp_context->ref_cnt = 1;

			memcpy(tmp_context->ptr, context->ptr, tmp_context->size);
			printf("Object %p: Deep copied context %p ptr %p size %d ref_cnt %d to context %p ptr %p ref_cnt %d\n",
			       this, context, context->ptr, context->size, context->ref_cnt, tmp_context, tmp_context->ptr,
			       tmp_context->ref_cnt);
			DisposeContext();
			context = tmp_context;
		}

		return context->ptr;
	}

	char operator[](int index)
	{
		if (!context)
			throw;

		if (index < 0 || index >= context->size)
			throw;

		printf ("Object %p, context %p ref_cnt %d,  indexing to %d, readonly\n",
		        this, context, context->ref_cnt, index);
		return ((char*)context->ptr)[index];
	}

	~Object()
	{
		DisposeContext();
	}
	protected:
	PtrContext *context;
};


int main(void)
{
	Object<void *> o;
	o = Object<void*>(10);
	Object<void *> o2 = o;
	Object<void *> o3;
	o = o3 = std::move(o2);
	*((char*)*o) = o3[0];

	Object<int[]> o4(new int[10]);
	return 0;
}