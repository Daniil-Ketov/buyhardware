import React from "react";

export const HeadlineCards = () => {
  return (
    <div className="max-w-[1640px] mx-auto p-4 py-12 grid md:grid-cols-3 gap-6">
      {/* Card */}
      <div className="rounded-xl relative">
        {/* Overlay */}
        <div className="absolute w-full h-full bg-black/50 rounded-xl text-white">
          <p className="font-bold text-2xl px-2 pt-4">Эсканор 2</p>
          <p className="px-2">Уже доступен</p>
          <button className="border-white bg-white text-black mx-2 absolute bottom-4 rounded-lg p-2">
            Заказать
          </button>
        </div>
        <img
          className="max-h-[160px] md:max-h-[200px] w-full object-cover rounded-xl"
          src="https://media.istockphoto.com/id/918951042/photo/super-computer-server-racks-in-datacenter-3d-illustration.jpg?s=612x612&w=0&k=20&c=k0MYXNmZBZyKFmeVSJbUl7vLKlPYwgR2s8VPTr3_3-E="
          alt="/"
        />
      </div>
      {/* Card */}
      <div className="rounded-xl relative">
        {/* Overlay */}
        <div className="absolute w-full h-full bg-black/50 rounded-xl text-white">
          <p className="font-bold text-2xl px-2 pt-4">Элеонора</p>
          <p className="px-2">Новейшее решение</p>
          <button className="border-white bg-white text-black mx-2 absolute bottom-4 rounded-lg p-2">
            Заказать
          </button>
        </div>
        <img
          className="max-h-[160px] md:max-h-[200px] w-full object-cover rounded-xl"
          src="https://media.istockphoto.com/id/1083935344/photo/workspace-with-computer-with-blank-white-screen-and-office-supplies-on-a-wooden-desk.jpg?s=612x612&w=0&k=20&c=Fs_En4aLsdmamkgXkzGDLIzrQrQoJcMX05l9naBreW4="
          alt="/"
        />
      </div>
      {/* Card */}
      <div className="rounded-xl relative">
        {/* Overlay */}
        <div className="absolute w-full h-full bg-black/50 rounded-xl text-white">
          <p className="font-bold text-2xl px-2 pt-4">Эсканор</p>
          <p className="px-2">Проверен временем</p>
          <button className="border-white bg-white text-black mx-2 absolute bottom-4 rounded-lg p-2">
            Заказать
          </button>
        </div>
        <img
          className="max-h-[160px] md:max-h-[200px] w-full object-cover rounded-xl"
          src="https://thumbs.dreamstime.com/b/data-center-computer-servers-6062358.jpg"
          alt="/"
        />
      </div>
    </div>
  );
};

export default HeadlineCards;
